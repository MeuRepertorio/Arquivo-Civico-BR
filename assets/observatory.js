/* Observatory Edition — client-side command palette. No tracking, no AI. */
(()=>{'use strict';
const actions=[
['⌂','Visão geral','Painel de dados e panorama do Congresso','#/inicio'],
['♙','Explorar políticos','Deputados, senadores e perfis históricos','#/politicos'],
['◈','Explorar partidos','Registros e trajetórias partidárias','#/partidos'],
['▤','Projetos e PECs','Proposições e tramitação na Câmara','#/legislacao'],
['≡','Votações','Consultar votos nominais com origem','#/votacoes'],
['⇄','Comparar pessoas','Colocar registros lado a lado','#/comparar'],
['◇','Investigações','Documentos, processos e critérios','#/investigacoes'],
['◎','Federações','Composição e registro no TSE','#/federacoes'],
['⊞','Fontes oficiais','Conferir origem dos dados','#/fontes'],
['⚑','Metodologia','Limites, atualização e verificabilidade','#/metodologia']];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const launch=document.createElement('button');launch.className='acb-launch';launch.type='button';launch.textContent='⌕  Explorar o acervo  ⌘ K';launch.setAttribute('aria-label','Abrir navegação rápida');document.body.append(launch);
let overlay=null;
function close(){overlay?.remove();overlay=null;launch.focus()}
function open(){if(overlay)return;overlay=document.createElement('div');overlay.className='acb-overlay';overlay.innerHTML='<div class="acb-command" role="dialog" aria-modal="true" aria-label="Navegação rápida"><div class="acb-command-head"><span>⌕</span><input aria-label="Pesquisar módulos" placeholder="O que você quer investigar?"><button type="button" data-close>ESC</button></div><div class="acb-command-list"></div><div class="acb-command-foot">↑ ↓ navegar · Enter abrir · Esc fechar · Dados públicos com fontes</div></div>';document.body.append(overlay);const input=overlay.querySelector('input'),list=overlay.querySelector('.acb-command-list');function draw(){const q=input.value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();const match=actions.filter(x=>(x[1]+' '+x[2]).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(q));list.innerHTML=match.length?match.map(x=>'<a href="'+x[3]+'"><span class="acb-command-icon">'+x[0]+'</span><span><b>'+esc(x[1])+'</b><small>'+esc(x[2])+'</small></span></a>').join(''):'<div style="padding:25px;color:#a5bfb4">Nenhuma área encontrada. Experimente outro termo.</div>'}input.addEventListener('input',draw);input.addEventListener('keydown',e=>{if(e.key==='Enter'){const a=list.querySelector('a');if(a){location.hash=a.getAttribute('href');close()}}});overlay.addEventListener('click',e=>{if(e.target===overlay||e.target.closest('[data-close]'))close();if(e.target.closest('.acb-command-list a'))close()});draw();input.focus()}
launch.onclick=open;document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();overlay?close():open()}else if(e.key==='Escape'&&overlay){e.preventDefault();close()}});
})();