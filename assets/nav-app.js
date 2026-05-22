const CAT_CN={"AI Agents":"AI 智能体","Web Frameworks":"建站框架","Docs & Knowledge":"文档知识库","No-Code & Admin":"低代码后台","Backend & Database":"后端数据库","Automation":"自动化","Data & Analytics":"数据分析","Deployment":"部署托管","Ops & Monitoring":"运维监控","Content & CMS":"内容 CMS"};
const CAT_EN={"AI Agents":"AI Agents","Web Frameworks":"Web Frameworks","Docs & Knowledge":"Docs & Knowledge","No-Code & Admin":"No-Code & Admin","Backend & Database":"Backend & Database","Automation":"Automation","Data & Analytics":"Data & Analytics","Deployment":"Deployment","Ops & Monitoring":"Ops & Monitoring","Content & CMS":"Content & CMS"};
const I18N={
 zh:{brand:'拾品号导航',submit:'提交收录',home:'首页',homeTitle:'GitHub 开源项目导航',homeSubtitle:'精选 AI、建站、后端、自动化、数据分析和部署运维工具',searchPlaceholder:'搜索项目、分类或直接回车跳转搜索...',filterPlaceholder:'搜索项目、标签、分类...',sideLeft:'开源<br>工具',sideRight:'快速<br>访问',friends:'友情链接',allProjects:'全部项目',aiNote:'AI 说明',sitemap:'站点地图',recommended:'推荐项目',all:'全部项目',count:'个项目',noMatch:'没有找到匹配项目',backHome:'返回首页',allTitle:'全部开源项目',allSubtitle:'搜索或按分类筛选，点击卡片直接打开 GitHub 项目。',submitTitle:'提交收录',submitSubtitle:'推荐好用的 GitHub 开源项目，后续可接入表单后端。',urlPlaceholder:'GitHub 项目地址：https://github.com/owner/repo',reasonPlaceholder:'推荐理由 / 分类',submitBtn:'提交',friendMsg:'友情链接入口已预留，后续可以添加合作站点。',uselessSite:'无聊网站',curatedLabel:'精选导航',directoryIntro:'按 WebStack 式分区浏览，快速找到值得收藏的开源项目。',guides:'使用指南',searchNav:'搜索',categoryNav:'分类目录',today:'今日',categories:'分类',engines:'搜索源',featuredSections:'分区浏览',open:'打开',daily:'上网，从拾品号导航开始。少一点广告，多一点直达。',dailyPick:'每日推荐项目',dailyReason:'今天重点看看这个项目：适合收藏、试用或加入你的开源工具箱。'},
 en:{brand:'ShipinHao Nav',submit:'Submit',home:'Home',homeTitle:'GitHub Open Source Navigation',homeSubtitle:'Curated AI, web, backend, automation, analytics, deployment and ops tools.',searchPlaceholder:'Search projects, categories, or press Enter to search...',filterPlaceholder:'Search by project, tag, or category...',sideLeft:'Open<br>Source',sideRight:'Quick<br>Access',friends:'Friends',allProjects:'All Projects',aiNote:'AI Notes',sitemap:'Sitemap',recommended:'Featured',all:'All Projects',count:'projects',noMatch:'No matching projects found.',backHome:'Back Home',allTitle:'All Open Source Projects',allSubtitle:'Search or filter by category. Click a card to open the GitHub project.',submitTitle:'Submit Project',submitSubtitle:'Recommend a useful GitHub open-source project. A backend form can be connected later.',urlPlaceholder:'GitHub project URL: https://github.com/owner/repo',reasonPlaceholder:'Reason / category',submitBtn:'Submit',friendMsg:'Friend links are reserved and can be added later.',uselessSite:'Useless Website',curatedLabel:'Curated directory',directoryIntro:'Browse by WebStack-style sections and find bookmark-worthy open-source projects faster.',guides:'Guides',searchNav:'Search',categoryNav:'Categories',today:'Today',categories:'categories',engines:'engines',featuredSections:'Browse by section',open:'Open',daily:'Start the web from ShipinHao Nav: less noise, faster access.',dailyPick:'Daily Project Pick',dailyReason:'Highlighted today: worth bookmarking, trying, or adding to your open-source toolbox.'}
};
const SEARCH_ENGINES=[
 {id:'github',label:'GitHub',url:q=>`https://github.com/search?q=${encodeURIComponent(q)}&type=repositories`},
 {id:'google',label:'Google',url:q=>`https://www.google.com/search?q=${encodeURIComponent(q+(lang==='zh'?' GitHub 开源':' GitHub open source'))}`},
 {id:'bing',label:'Bing',url:q=>`https://www.bing.com/search?q=${encodeURIComponent(q+(lang==='zh'?' GitHub 开源':' GitHub open source'))}`},
 {id:'metaso',label:'秘塔 AI',url:q=>`https://metaso.cn/?q=${encodeURIComponent(q)}`},
 {id:'npm',label:'npm',url:q=>`https://www.npmjs.com/search?q=${encodeURIComponent(q)}`},
 {id:'docker',label:'Docker',url:q=>`https://hub.docker.com/search?q=${encodeURIComponent(q)}`}
];
let projects=[],active='__featured',engine='github',lang=localStorage.getItem('lang')||((navigator.language||'').toLowerCase().startsWith('zh')?'zh':'en');
window.__lang=lang;
const $=s=>document.querySelector(s);
function t(k){return (I18N[lang]&&I18N[lang][k])||I18N.zh[k]||k}
function catLabel(c){return (lang==='zh'?CAT_CN:CAT_EN)[c]||c}
function cats(){return [...new Set(projects.map(p=>p.category))]}
function applyI18n(){document.documentElement.lang=lang==='zh'?'zh-CN':'en'; document.title=lang==='zh'?'拾品号导航 - GitHub 开源项目导航':'ShipinHao Nav - GitHub Open Source Navigation'; document.querySelectorAll('[data-i18n]').forEach(el=>el.textContent=t(el.dataset.i18n)); document.querySelectorAll('[data-i18n-html]').forEach(el=>el.innerHTML=t(el.dataset.i18nHtml)); document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>el.placeholder=t(el.dataset.i18nPlaceholder)); const b=$('#langToggle'); if(b)b.textContent=lang==='zh'?'EN':'中文'; const d=$('#dailyLine'); if(d)d.textContent=t('daily'); window.__lang=lang;}
function descText(p){return lang==='zh'?(p.desc_cn||p.desc):p.desc}
function card(p){const desc=descText(p);const tags=(p.tags||[]).slice(0,2).map(x=>`<span>${x}</span>`).join('');return `<a class="link-item" href="${p.url}" target="_blank" rel="noopener" title="${p.name} - ${desc}"><div class="card-head"><span class="site-icon">${p.icon||p.name.slice(0,2).toUpperCase()}</span><div class="title-wrap"><strong>${p.name}</strong><em>${catLabel(p.category)}</em></div></div><p class="link-desc">${desc}</p><div class="tag-row">${tags}<b>${t('open')} ↗</b></div></a>`}
function renderTop(){const nav=$('#topCategories'); if(!nav)return; const list=['__featured',...cats()]; nav.innerHTML=list.map(c=>`<button class="${c===active?'active':''}" data-cat="${c}">${c==='__featured'?t('recommended'):catLabel(c)}</button>`).join(''); nav.querySelectorAll('button').forEach(b=>b.onclick=()=>{active=b.dataset.cat; const inp=$('#searchInput'); if(inp)inp.value=''; renderAll();});}
function renderSidebar(){const side=$('#categorySidebar'); if(!side)return; const list=['__featured',...cats()]; side.innerHTML=`<div class="side-title">${t('categoryNav')}</div>`+list.map(c=>`<button class="${c===active?'active':''}" data-cat="${c}"><span>${c==='__featured'?'★':'#'}</span>${c==='__featured'?t('recommended'):catLabel(c)}</button>`).join(''); side.querySelectorAll('button').forEach(b=>b.onclick=()=>{active=b.dataset.cat; const inp=$('#searchInput'); if(inp)inp.value=''; renderAll(); window.scrollTo({top:0,behavior:'smooth'});});}
function renderEngines(){const box=document.querySelector('.engine-tabs'); if(!box)return; box.innerHTML=SEARCH_ENGINES.map(e=>`<button class="${e.id===engine?'active':''}" data-engine="${e.id}">${e.label}</button>`).join(''); box.querySelectorAll('button').forEach(b=>b.onclick=()=>{engine=b.dataset.engine; renderEngines();});}
function currentTitle(){if(location.pathname.startsWith('/projects/') && active==='__featured') return t('all'); return active==='__featured'?t('recommended'):catLabel(active)}
function filteredList(){const q=($('#searchInput')?.value||new URLSearchParams(location.search).get('q')||'').toLowerCase(); const urlCat=new URLSearchParams(location.search).get('category'); if(urlCat && active==='__featured') active=urlCat; let list=projects.filter(p=>{const byCat=active==='__featured'?p.featured:(active==='__all'||!active?true:p.category===active); const hay=[p.name,p.desc,p.category,catLabel(p.category),p.category_cn,...(p.tags||[])].join(' ').toLowerCase(); return byCat && hay.includes(q)}); if(location.pathname.startsWith('/projects/') && active==='__featured') list=projects.filter(p=>[p.name,p.desc,p.category,catLabel(p.category),p.category_cn,...(p.tags||[])].join(' ').toLowerCase().includes(q)); return {list,q};}
function renderStats(){const stats=$('#statsRow'); if(!stats)return; const total=projects.length, catCount=cats().length; const date=new Date().toLocaleDateString(lang==='zh'?'zh-CN':'en-US',{month:'short',day:'numeric'}); stats.innerHTML=`<span>${total} ${t('count')}</span><span>${catCount} ${t('categories')}</span><span>${SEARCH_ENGINES.length} ${t('engines')}</span><span>${t('today')} ${date}</span>`;}
function renderSections(q=''){const wrap=$('#sectionList'); if(!wrap)return; if(location.pathname.startsWith('/projects/') || q || active!=='__featured'){wrap.innerHTML=''; return;} const groups=cats().map(c=>{const items=projects.filter(p=>p.category===c).slice(0,8); if(!items.length)return ''; return `<section class="nav-section" id="cat-${c.replace(/[^a-z0-9]+/gi,'-')}"><h2><span>${catLabel(c)}</span><small>${items.length} / ${projects.filter(p=>p.category===c).length}</small></h2><div class="mini-grid">${items.map(card).join('')}</div></section>`}).join(''); wrap.innerHTML=`<div class="section-heading">${t('featuredSections')}</div>${groups}`;}

function dailyProject(){
  if(!projects.length)return null;
  const start=new Date(new Date().getFullYear(),0,0);
  const day=Math.floor((new Date()-start)/86400000);
  const pool=projects.filter(p=>p.featured)||projects;
  return pool[day%pool.length];
}
function renderDailyRecommend(){
  const box=$('#dailyRecommend'); if(!box)return;
  const p=dailyProject(); if(!p){box.innerHTML=''; return;}
  const desc=descText(p);
  const tags=(p.tags||[]).slice(0,3).map(x=>`<span>${x}</span>`).join('');
  box.innerHTML=`<a class="daily-card" href="${p.url}" target="_blank" rel="noopener"><div class="daily-badge">★ ${t('dailyPick')}</div><div class="daily-main"><span class="site-icon daily-icon">${p.icon||p.name.slice(0,2).toUpperCase()}</span><div><strong>${p.name}</strong><em>${catLabel(p.category)}</em><p>${desc}</p><small>${t('dailyReason')}</small><div class="tag-row daily-tags">${tags}<b>${t('open')} ↗</b></div></div></div></a>`;
}
function render(){const grid=$('#linkGrid'); if(!grid)return; const {list,q}=filteredList(); grid.innerHTML=list.map(card).join('')||`<p style="grid-column:1/-1;text-align:center;color:#fff">${t('noMatch')}</p>`; $('#activeTitle') && ($('#activeTitle').textContent=currentTitle()); $('#resultCount') && ($('#resultCount').textContent=`${list.length} ${t('count')}`); renderSections(q); renderStats(); renderDailyRecommend();}
function renderAll(){applyI18n(); renderTop(); renderSidebar(); renderEngines(); render();}
function doSearch(){const q=$('#searchInput')?.value.trim(); if(!q)return; const found=SEARCH_ENGINES.find(e=>e.id===engine)||SEARCH_ENGINES[0]; window.open(found.url(q), '_blank','noopener');}
function switchLang(){lang=lang==='zh'?'en':'zh'; localStorage.setItem('lang',lang); renderAll();}
function initEffects(){
  const fine=matchMedia('(pointer:fine)').matches;
  document.addEventListener('pointermove',e=>{
    document.documentElement.style.setProperty('--mx',`${e.clientX}px`);
    document.documentElement.style.setProperty('--my',`${e.clientY}px`);
    if(!fine)return;
    const dot=document.createElement('span'); dot.className='cursor-trail'; dot.style.left=e.clientX+'px'; dot.style.top=e.clientY+'px'; document.body.appendChild(dot); setTimeout(()=>dot.remove(),780);
    if(Math.random()<0.23){const s=document.createElement('span'); s.className='sparkle'; s.style.left=e.clientX+'px'; s.style.top=e.clientY+'px'; s.style.setProperty('--dx',`${(Math.random()-.5)*70}px`); s.style.setProperty('--dy',`${(Math.random()-.5)*70}px`); document.body.appendChild(s); setTimeout(()=>s.remove(),1000);}
  },{passive:true});
  document.addEventListener('pointermove',e=>{const card=e.target.closest?.('.link-item'); if(!card)return; const r=card.getBoundingClientRect(); card.style.setProperty('--card-x',`${e.clientX-r.left}px`); card.style.setProperty('--card-y',`${e.clientY-r.top}px`);},{passive:true});
}
function initBackTop(){const btn=$('#backTop'); if(!btn)return; const toggle=()=>btn.classList.toggle('show',scrollY>520); addEventListener('scroll',toggle,{passive:true}); btn.onclick=()=>scrollTo({top:0,behavior:'smooth'}); toggle();}
async function init(){initEffects(); initBackTop(); projects=await (await fetch('/data/projects.json')).json(); if(location.pathname.startsWith('/projects/')) active='__featured'; renderAll(); $('#langToggle')?.addEventListener('click',switchLang); $('#searchInput')?.addEventListener('input',()=>{render();}); $('#searchInput')?.addEventListener('keydown',e=>{if(e.key==='Enter')doSearch();}); $('#searchBtn')?.addEventListener('click',doSearch); $('#friendBtn')?.addEventListener('click',()=>alert(t('friendMsg')));}
init();
