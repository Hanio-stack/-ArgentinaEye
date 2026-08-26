#!/usr/bin/env python3
from __future__ import annotations
import argparse,copy,email.utils,html,json,re,sys,urllib.parse,urllib.request,xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime,timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
ROOT=Path(__file__).resolve().parents[1] if Path(__file__).resolve().parent.name=='scripts' else Path.cwd();LATEST=ROOT/'public'/'data'/'latest.json';HISTORY=ROOT/'public'/'data'/'history';UA='ArgentinaEye/0.2 (+personal research dashboard; GitHub Actions)';TIMEOUT=18
INFLATION_URL='https://apis.datos.gob.ar/series/api/series?'+urllib.parse.urlencode({'ids':'145.3_INGNACUAL_DICI_M_38','last':13});BCRA_CATALOG='https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias?limit=3000';BCRA_BASE='https://api.bcra.gob.ar/estadisticas/v4.0/Monetarias'
FISCAL_URL='https://www.argentina.gob.ar/economia/politicafiscal';ENERGY_NEWS_URL='https://www.argentina.gob.ar/economia/energia/noticias';RIGI_URL='https://www.argentina.gob.ar/economia/rigi';RIGI_BASELINE_URL='https://www.argentina.gob.ar/noticias/el-ministerio-de-economia-lanzo-una-web-oficial-con-la-informacion-de-los-proyectos-del';ECONOMY_NEWS_URL='https://www.argentina.gob.ar/economia/noticias';CAMMESA_DEMAND_CANDIDATES=['https://api.cammesa.com/demanda-svc/demanda/ObtieneDemandaYTemperaturaRegionById?id_region=1002','https://api.cammesa.com/demanda-svc/demanda/ObtieneDemandaYTemperaturaRegion?id_region=1002'];CAMMESA_REPORT_URL='https://cammesaweb.cammesa.com/informe-sintesis-mensual/'
NEWS_QUERIES={'politics':'Javier Milei approval poll Argentina','fiscal_balance':'Argentina fiscal surplus Milei economy','vaca_muerta_oil':'Vaca Muerta production Argentina','rigi_investment':'Argentina RIGI investment approved','electricity':'Argentina electricity market reform CAMMESA energy','big_money':'(Peter Thiel OR Harold Hamm OR Chevron OR Mercuria OR Eni OR XRG) Argentina Vaca Muerta investment'};ENTITY_ALIASES={'Thiel':['peter thiel','thiel macro'],'Hamm':['harold hamm','continental resources'],'Chevron':['chevron'],'Mercuria':['mercuria'],'Eni':[' eni ','eni ',' eni'],'XRG':['xrg']}
MONTHS={'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
@dataclass
class FetchResult: ok:bool;name:str;note:str=''
class PageParser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.links=[];self.href=None;self.anchor=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.href=dict(attrs).get('href');self.anchor=[]
 def handle_endtag(self,tag):
  if tag=='a' and self.href:self.links.append((self.href,' '.join(self.anchor).strip()));self.href=None;self.anchor=[]
 def handle_data(self,data):
  t=data.strip()
  if t:self.parts.append(t)
  if self.href and t:self.anchor.append(t)
def get_bytes(url):
 req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/json, application/xml, text/xml, text/html, */*'});return urllib.request.urlopen(req,timeout=TIMEOUT).read()
def get_json(url):return json.loads(get_bytes(url).decode('utf-8'))
def get_html(url):return get_bytes(url).decode('utf-8','replace')
def parse_page(raw):
 p=PageParser();p.feed(raw);return re.sub(r'\s+',' ',' '.join(p.parts)).strip(),p.links
def spanish_number(s):
 s=re.sub(r'[^0-9,.-]','',s)
 if not s:return None
 if ',' in s and '.' in s:s=s.replace('.','').replace(',','.')
 elif ',' in s:s=s.replace(',','.')
 elif s.count('.')>=1 and all(len(x)==3 for x in s.split('.')[1:]):s=s.replace('.','')
 return float(s)
def month_period(name,now=None):
 now=now or datetime.now(timezone.utc);m=MONTHS.get(name.lower())
 if not m:return None
 y=now.year-1 if now.month<=2 and m>=11 else now.year
 return f'{y:04d}-{m:02d}'
def publication_period(text,now=None):
 m=re.search(r'(\d{1,2})\s+de\s+('+ '|'.join(MONTHS) +r')\s+de\s+(\d{4})',text,re.I)
 return f'{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}' if m else None
def load_previous():return json.loads(LATEST.read_text(encoding='utf-8')) if LATEST.exists() else {'metrics':[],'news':[]}
def metric_map(data):return {m['id']:m for m in data.get('metrics',[])}
def set_metric(data,metric):
 metrics=metric_map(data);metrics[metric['id']]=metric;order=['milei_approval','inflation_monthly','international_reserves','fiscal_balance','vaca_muerta_oil','rigi_investment','electricity'];data['metrics']=[metrics[i] for i in order if i in metrics]
def fetch_inflation():
 p=get_json(INFLATION_URL);rows=p.get('data') or []
 if rows and isinstance(rows[0],list) and rows[0] and isinstance(rows[0][0],list):rows=rows[0]
 clean=[(str(r[0]),float(r[1])) for r in rows if isinstance(r,list) and len(r)>=2 and r[1] is not None]
 if not clean:raise ValueError('INDEC series returned no observations')
 d,v=clean[-1];pv=clean[-2][1] if len(clean)>1 else None;trend=[x[1] for x in clean[-3:]];signal='positive' if len(trend)>=2 and trend[-1]<trend[-2] else 'neutral';cv=lambda x:round(x*100 if abs(x)<1 else x,2)
 return {'id':'inflation_monthly','theme':'MACRO · 15%','label':'Inflation','value':cv(v),'unit':'% m/m','period':d[:7],'previous':cv(pv) if pv is not None else None,'change':round((v-pv)*100 if abs(v)<1 else v-pv,2) if pv is not None else None,'change_unit':'pp','thesis_signal':signal,'status':'fresh','detail':'Official national monthly CPI variation.','source':{'name':'INDEC / Datos Argentina','url':INFLATION_URL},'series':[cv(x) for _,x in clean[-6:]]}
def _bcra_reserve_catalog_item(p):
 c=[r for r in p.get('results',[]) if 'reserv' in str(r.get('descripcion','')).lower() and 'intern' in str(r.get('descripcion','')).lower()]
 if not c:raise ValueError('BCRA reserves variable not found')
 c.sort(key=lambda r:0 if int(r.get('idVariable',999999))==1 else 1);return c[0]
def _extract_bcra_points(p):
 out=[]
 for item in p.get('results') or []:
  if isinstance(item,dict) and 'detalle' in item:
   for x in item.get('detalle') or []:
    if x.get('fecha') and x.get('valor') is not None:out.append((str(x['fecha']),float(x['valor'])))
  elif isinstance(item,dict) and item.get('fecha') and item.get('valor') is not None:out.append((str(item['fecha']),float(item['valor'])))
 out.sort(key=lambda x:x[0]);return out
def fetch_reserves():
 item=_bcra_reserve_catalog_item(get_json(BCRA_CATALOG));vid=int(item['idVariable']);points=_extract_bcra_points(get_json(f'{BCRA_BASE}/{vid}?limit=60'))
 if not points:
  lv,ld=item.get('ultValorInformado'),item.get('ultFechaInformada')
  if lv is None or not ld:raise ValueError('BCRA reserves returned no observations')
  points=[(str(ld),float(lv))]
 d,v=points[-1];base=points[max(0,len(points)-31)][1] if len(points)>=2 else None;ch=((v/base)-1)*100 if base else None;signal='neutral' if ch is None or -1<ch<1 else('positive' if ch>=1 else 'negative')
 return {'id':'international_reserves','theme':'MACRO · 15%','label':'BCRA reserves','value':round(v/1000,2),'unit':'USD bn','period':d,'previous':round(base/1000,2) if base else None,'change':round(ch,2) if ch is not None else None,'change_unit':'% ~30d','thesis_signal':signal,'status':'fresh','detail':'Official BCRA international reserves.','source':{'name':'BCRA Statistics API','url':f'{BCRA_BASE}/{vid}'},'series':[round(x/1000,2) for _,x in points[-30:]]}
def parse_fiscal_html(raw,now=None):
 text,_=parse_page(raw);m=re.search(r'([+\-])?\s*\$?\s*([\d.,]+)\s*millones\s+Resultado primario\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+)',text,re.I)
 if not m:m=re.search(r'Resultado primario\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+).*?([+\-])?\s*\$?\s*([\d.,]+)\s*millones',text,re.I)
 if not m:raise ValueError('Fiscal primary balance not found')
 if m.lastindex==3 and m.group(1) and m.group(1).lower() in MONTHS:month,sign,num=m.group(1),m.group(2),m.group(3)
 else:sign,num,month=m.group(1) or '+',m.group(2),m.group(3)
 value=spanish_number(num);value=-value if sign=='-' else value;period=month_period(month,now);signal='positive' if value>0 else 'negative'
 return {'id':'fiscal_balance','theme':'MACRO · 15%','label':'Primary fiscal balance','value':round(value/1_000_000,3),'unit':'ARS tn','period':period,'previous':None,'change':None,'thesis_signal':signal,'status':'fresh','detail':f'Official SPN primary balance: ARS {value:,.0f} million.','source':{'name':'Ministerio de Economía · Política Fiscal','url':FISCAL_URL}}
def fetch_fiscal():return parse_fiscal_html(get_html(FISCAL_URL))
def _official_links(raw,base,keywords):
 _,links=parse_page(raw);out=[];seen=set()
 for href,title in links:
  u=urllib.parse.urljoin(base,href);t=title.lower()
  if u in seen or '/noticias/' not in u:continue
  if any(k in t or k in u.lower() for k in keywords):seen.add(u);out.append((u,title))
 return out
def parse_vaca_html(raw,url=ENERGY_NEWS_URL,title='',now=None):
 text,_=parse_page(raw);m=re.search(r'Vaca Muerta.{0,260}?(?:alcanz\w*|ritmo de producci[oó]n de|producci[oó]n de)\s*(?:los\s*)?([\d.,]+)\s*mil barriles diarios',text,re.I)
 if not m:raise ValueError('Vaca Muerta oil rate not found')
 value=spanish_number(m.group(1));window=text[m.start():m.end()+260];y=re.search(r'(?:incremento|aumento|crecimiento)[^%]{0,90}?([\d.,]+)\s*%',window,re.I);yoy=spanish_number(y.group(1)) if y else None;low=(title+' '+text[:350]).lower();mon=next((x for x in MONTHS if re.search(r'\b'+x+r'\b',low)),None);period=month_period(mon,now) if mon else publication_period(text,now);signal='positive' if yoy is None or yoy>=5 else('negative' if yoy<0 else 'neutral')
 return {'id':'vaca_muerta_oil','theme':'VIST · 10%','label':'Vaca Muerta oil','value':round(value,1),'unit':'k bpd','period':period,'previous':None,'change':round(yoy,1) if yoy is not None else None,'change_kind':'yoy_pct','thesis_signal':signal,'status':'fresh','detail':'Official Vaca Muerta oil production rate.','source':{'name':'Secretaría de Energía','url':url}}
def fetch_vaca_muerta():
 listing=get_html(ENERGY_NEWS_URL);links=_official_links(listing,ENERGY_NEWS_URL,['produccion','producción','petroleo','petróleo','vaca-muerta']);errors=[]
 for u,t in links[:12]:
  try:return parse_vaca_html(get_html(u),u,t)
  except Exception as e:errors.append(str(e))
 raise ValueError('No parsable official Vaca Muerta article: '+('; '.join(errors[:2]) or 'no candidates'))
def parse_rigi_html(raw,url=RIGI_URL,now=None):
 text,_=parse_page(raw);patterns=[r'Proyectos aprobados.{0,140}?Cantidad\s+(\d+).{0,160}?Inversi[oó]n total\s+USD\s*([\d.,]+)\s*M',r'Proyectos aprobados por resoluci[oó]n\s+(\d+)\s+proyectos\s+US\$\s*([\d.,]+)\s+millones de inversi[oó]n']
 for pat in patterns:
  m=re.search(pat,text,re.I)
  if not m:continue
  count=int(m.group(1));amount=spanish_number(m.group(2))
  if count<=0 or amount<=0:continue
  period=publication_period(text,now);return {'id':'rigi_investment','theme':'CAPITAL · 10%','label':'RIGI approved investment','value':round(amount/1000,3),'unit':'USD bn','period':period,'previous':None,'change':None,'thesis_signal':'positive','status':'fresh','detail':f'{count} approved RIGI projects; official committed investment total.','source':{'name':'Ministerio de Economía · RIGI','url':url},'project_count':count}
 raise ValueError('RIGI cumulative totals not found')
def fetch_rigi():
 candidates=[(RIGI_URL,get_html(RIGI_URL))]
 try:
  for u,t in _official_links(get_html(ECONOMY_NEWS_URL),ECONOMY_NEWS_URL,['rigi'])[:10]:candidates.append((u,get_html(u)))
 except Exception:pass
 candidates.append((RIGI_BASELINE_URL,get_html(RIGI_BASELINE_URL)));parsed=[]
 for u,raw in candidates:
  try:parsed.append(parse_rigi_html(raw,u))
  except Exception:pass
 if not parsed:raise ValueError('No official RIGI cumulative total could be parsed')
 return max(parsed,key=lambda x:(x.get('project_count',0),x.get('value',0)))
def _walk_json(obj):
 if isinstance(obj,dict):
  yield obj
  for v in obj.values():yield from _walk_json(v)
 elif isinstance(obj,list):
  for v in obj:yield from _walk_json(v)
def _demand_candidates(obj):
 vals=[]
 for d in _walk_json(obj):
  for k,v in d.items():
   kl=str(k).lower()
   if isinstance(v,(int,float)) and any(x in kl for x in ['demanda','potencia','mw']) and 1000<float(v)<50000:vals.append(float(v))
 return vals
def fetch_electricity():
 errs=[]
 for u in CAMMESA_DEMAND_CANDIDATES:
  try:
   p=get_json(u);vals=_demand_candidates(p)
   if not vals:raise ValueError('no MW demand values')
   value=vals[-1];return {'id':'electricity','theme':'CEPU · 10%','label':'SADI electricity demand','value':round(value,0),'unit':'MW live','period':datetime.now(timezone.utc).strftime('%Y-%m-%d'),'previous':None,'change':None,'thesis_signal':'neutral','status':'fresh','detail':'CAMMESA public real-time system demand. Monthly reform/news context is attached separately.','source':{'name':'CAMMESA public API','url':u}}
  except Exception as e:errs.append(str(e))
 raw=get_html(CAMMESA_REPORT_URL);text,_=parse_page(raw);m=re.search(r'Informe Mensual\s+([A-Za-zÁÉÍÓÚáéíóú]+)\s+(20\d{2})',text,re.I)
 if not m:raise ValueError('CAMMESA demand API and monthly report discovery failed: '+'; '.join(errs[:2]))
 period=f"{int(m.group(2)):04d}-{MONTHS.get(m.group(1).lower(),1):02d}";return {'id':'electricity','theme':'CEPU · 10%','label':'Power demand / reform','value':None,'unit':None,'period':period,'previous':None,'change':None,'thesis_signal':'neutral','status':'fresh','detail':f'CAMMESA monthly system report published for {period}; live MW endpoint unavailable this run.','source':{'name':'CAMMESA monthly report','url':CAMMESA_REPORT_URL}}
def google_news_rss(query,limit=6):
 url=f'https://news.google.com/rss/search?q={urllib.parse.quote_plus(query)}&hl=en&gl=US&ceid=US:en';root=ET.fromstring(get_bytes(url));items=[]
 for item in root.findall('./channel/item')[:limit]:
  title=(item.findtext('title') or '').strip();link=(item.findtext('link') or '').strip();raw=(item.findtext('pubDate') or '').strip();sn=item.find('source');source=(sn.text or '').strip() if sn is not None else 'Google News';published=raw
  if raw:
   try:published=email.utils.parsedate_to_datetime(raw).astimezone(timezone.utc).strftime('%Y-%m-%d')
   except Exception:pass
  items.append({'title':title,'url':link,'published':published,'source':source})
 return items
def match_entities(title):
 text=f' {title.lower()} ';return [n for n,a in ENTITY_ALIASES.items() if any(x in text for x in a)]
def collect_news():
 all_items=[];topics={};health=[];seen=set()
 for topic,q in NEWS_QUERIES.items():
  try:
   items=google_news_rss(q);health.append(FetchResult(True,f'News: {topic}',f'{len(items)} items'))
   if items:topics[topic]=items[0]
   for item in items:
    key=re.sub(r'\W+',' ',item['title'].lower()).strip()
    if key in seen:continue
    seen.add(key);item['topic']=topic;item['entities']=match_entities(item['title'])
    if topic=='big_money' or item['entities']:all_items.append(item)
  except Exception as e:health.append(FetchResult(False,f'News: {topic}',str(e)[:90]))
 all_items.sort(key=lambda x:x.get('published',''),reverse=True);return all_items[:20],topics,health
def inflation_factor(m):
 if m.get('value') is None:return None
 v=float(m['value']);base=100 if v<=1.5 else 80 if v<=2.5 else 60 if v<=4 else 35 if v<=7 else 10;s=m.get('series') or []
 if len(s)>=3 and s[-1]<s[-2]<s[-3]:base+=5
 elif len(s)>=3 and s[-1]>s[-2]>s[-3]:base-=5
 return max(0,min(100,base))
def reserves_factor(m):
 c=m.get('change')
 if c is None:return 60 if m.get('value') is not None else None
 c=float(c);return 90 if c>=5 else 75 if c>=1 else 60 if c>=-1 else 40 if c>=-5 else 20
def categorical_factor(m,positive=75,neutral=55,negative=30):
 if m.get('status')=='unavailable' and m.get('value') is None and not m.get('latest_event'):return None
 return {'positive':positive,'neutral':neutral,'negative':negative}.get(m.get('thesis_signal'),neutral)
def weighted_score(parts):
 a=[(s,w) for s,w in parts if s is not None]
 if not a:return 50.0,0.0
 return round(sum(float(s)*w for s,w in a)/sum(w for _,w in a),1),round(sum(w for _,w in a)/sum(w for _,w in parts),2)
def build_scores(data):
 m=metric_map(data);inf=inflation_factor(m.get('inflation_monthly',{}));res=reserves_factor(m.get('international_reserves',{}));pol=categorical_factor(m.get('milei_approval',{}));fis=categorical_factor(m.get('fiscal_balance',{}));vaca=categorical_factor(m.get('vaca_muerta_oil',{}),90,55,20);rigi=categorical_factor(m.get('rigi_investment',{}),85,55,25);elec=categorical_factor(m.get('electricity',{}),75,55,30);capital=70 if data.get('news') else 55;a,ac=weighted_score([(pol,20),(inf,15),(res,15),(fis,15),(vaca,10),(rigi,10),(elec,10),(capital,5)]);v,vc=weighted_score([(a,25),(vaca,30),(rigi,15),(capital,15),(pol,15)]);c,cc=weighted_score([(a,20),(elec,45),(rigi,15),(pol,15),(capital,5)]);return {'argentina':{'label':'Argentina','score':a,'confidence':ac},'vist':{'label':'VIST','score':v,'confidence':vc},'cepu':{'label':'CEPU','score':c,'confidence':cc}}
def attach_topic_events(data,topics):
 mapping={'milei_approval':'politics','fiscal_balance':'fiscal_balance','vaca_muerta_oil':'vaca_muerta_oil','rigi_investment':'rigi_investment','electricity':'electricity'};m=metric_map(data)
 for mid,t in mapping.items():
  if mid in m and t in topics:m[mid]['latest_event']=topics[t]
def build_today(cur,prev):
 rows=[];pm=metric_map(prev)
 for m in cur.get('metrics',[]):
  old=pm.get(m['id'],{});changed=m.get('value')!=old.get('value') or m.get('period')!=old.get('period') or m.get('latest_event',{}).get('title')!=old.get('latest_event',{}).get('title')
  if changed:rows.append({'title':m['label'],'detail':m.get('latest_event',{}).get('title') or m.get('detail') or 'Updated observation','signal':m.get('thesis_signal') if m.get('thesis_signal') in {'positive','negative','neutral'} else 'neutral'})
 if cur.get('news') and cur.get('news')!=prev.get('news'):
  i=cur['news'][0];rows.append({'title':'Big Money','detail':i['title'],'signal':'positive' if i.get('entities') else 'neutral'})
 return rows[:5]
def main():
 p=argparse.ArgumentParser();p.add_argument('--offline',action='store_true');args=p.parse_args();prev=load_previous();data=copy.deepcopy(prev);health=[]
 if not args.offline:
  adapters=[('INDEC inflation',fetch_inflation),('BCRA reserves',fetch_reserves),('Fiscal balance',fetch_fiscal),('Vaca Muerta oil',fetch_vaca_muerta),('RIGI',fetch_rigi),('CAMMESA demand',fetch_electricity)]
  for name,func in adapters:
   try:set_metric(data,func());health.append(FetchResult(True,name))
   except Exception as e:health.append(FetchResult(False,name,str(e)[:120]))
  news,topics,nh=collect_news();health+=nh
  if news:data['news']=news
  attach_topic_events(data,topics)
 else:health.append(FetchResult(True,'Offline mode','network skipped'))
 data.update(version=2,mode='offline' if args.offline else 'auto',generated_at=datetime.now(timezone.utc).isoformat().replace('+00:00','Z'));data['scores']=build_scores(data);data['today']=build_today(data,prev);data['source_health']=[{'name':h.name,'ok':h.ok,'note':h.note} for h in health];LATEST.parent.mkdir(parents=True,exist_ok=True);HISTORY.mkdir(parents=True,exist_ok=True);text=json.dumps(data,ensure_ascii=False,indent=2)+'\n';LATEST.write_text(text,encoding='utf-8');(HISTORY/f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.json").write_text(text,encoding='utf-8');print(f'wrote {LATEST}');return 0
if __name__=='__main__':sys.exit(main())
