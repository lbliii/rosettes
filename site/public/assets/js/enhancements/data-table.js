(function(){'use strict';if(!window.BengalUtils){console.error('BengalUtils not loaded - data-table.js requires utils.js');return;}
const{log,debounce,ready}=window.BengalUtils;function initDataTables(){if(typeof Tabulator==='undefined'){console.error('Tabulator library not loaded - data tables will not work');return;}
const tableWrappers=document.querySelectorAll('.bengal-data-table-wrapper');if(tableWrappers.length===0){return;}
log(`Initializing ${tableWrappers.length}data table(s)`);tableWrappers.forEach(wrapper=>{initSingleTable(wrapper);});}
function initSingleTable(wrapper){const tableId=wrapper.getAttribute('data-table-id');const tableElement=wrapper.querySelector(`#${tableId}`);const searchInput=wrapper.querySelector(`#${tableId}-search`);const configScript=wrapper.querySelector(`script[data-table-config="${tableId}"]`);if(!tableElement||!configScript){console.error(`Data table ${tableId}missing required elements`);return;}
let config;try{config=JSON.parse(configScript.textContent);}catch(e){console.error(`Failed to parse config for table ${tableId}:`,e);return;}
config=applyBengalTheme(config);let table;try{table=new Tabulator(tableElement,config);}catch(e){console.error(`Failed to initialize table ${tableId}:`,e);return;}
if(searchInput&&config.data){searchInput.addEventListener('input',debounce(function(e){table.setFilter(matchAny,e.target.value);},300));searchInput.addEventListener('keydown',function(e){if(e.key==='Escape'){searchInput.value='';table.clearFilter();}});}
wrapper._tabulatorInstance=table;log(`Initialized table ${tableId}`);}
function applyBengalTheme(config){if(config.columns){config.columns=config.columns.map(col=>({...col,resizable:true,headerSort:config.sort!==false,headerTooltip:true,}));}
if(config.pagination){config.paginationMode='local';config.paginationSizeSelector=[10,25,50,100,200];config.paginationCounter='rows';}
config.tabEndNewRow=false;config.keybindings={navPrev:"shift + 9",navNext:9,navUp:38,navDown:40,};config.responsiveLayout='collapse';config.responsiveLayoutCollapseStartOpen=false;config.virtualDom=true;config.virtualDomBuffer=300;return config;}
function matchAny(data,filterParams){if(!filterParams||typeof filterParams!=='string'||filterParams.trim()===''){return true;}
const searchTerm=filterParams.toLowerCase();return Object.values(data).some(value=>{if(value===null||value===undefined){return false;}
return String(value).toLowerCase().includes(searchTerm);});}
function exportTable(tableId,format='csv'){const wrapper=document.querySelector(`[data-table-id="${tableId}"]`);if(!wrapper||!wrapper._tabulatorInstance){console.error(`Table ${tableId}not found`);return;}
const table=wrapper._tabulatorInstance;switch(format){case'csv':table.download('csv',`${tableId}.csv`);break;case'json':table.download('json',`${tableId}.json`);break;default:console.warn(`Export format ${format}not supported`);}}
ready(initDataTables);window.BengalDataTable={init:initDataTables,export:exportTable,};})();