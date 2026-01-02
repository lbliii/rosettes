(function(){'use strict';class SessionPathTracker{constructor(options={}){this.storageKey=options.storageKey||'bengal_session_previous_page';this.previousPage=this.loadPreviousPage();}
loadPreviousPage(){try{const stored=sessionStorage.getItem(this.storageKey);if(stored){return stored;}}catch(e){console.warn('SessionPathTracker: Failed to load previous page from sessionStorage',e);}
return null;}
savePreviousPage(){try{if(this.previousPage){sessionStorage.setItem(this.storageKey,this.previousPage);}else{sessionStorage.removeItem(this.storageKey);}}catch(e){console.warn('SessionPathTracker: Failed to save previous page to sessionStorage',e);}}
normalizeUrl(url){if(!url)return'';let normalized=url;if(normalized.startsWith('http://')||normalized.startsWith('https://')){try{const urlObj=new URL(normalized);normalized=urlObj.pathname;}catch(e){const match=normalized.match(/https?:\/\/[^\/]+(\/.*)/);if(match){normalized=match[1];}}}
normalized=normalized.replace(/\/+$/,'')||'/';if(!normalized.startsWith('/')){normalized='/'+normalized;}
normalized=normalized.split('#')[0];return normalized;}
trackPage(url){const normalizedUrl=this.normalizeUrl(url);if(this.previousPage===normalizedUrl){return;}
this.previousPage=normalizedUrl;this.savePreviousPage();}
getPreviousPage(){return this.previousPage;}
isPreviousPage(url){if(!this.previousPage)return false;const normalizedUrl=this.normalizeUrl(url);return this.previousPage===normalizedUrl;}
clearPreviousPage(){this.previousPage=null;this.savePreviousPage();}}
window.BengalSessionPathTracker=SessionPathTracker;if(typeof window!=='undefined'){const tracker=new SessionPathTracker();const currentUrl=window.location.pathname;tracker.trackPage(currentUrl);window.bengalSessionPath=tracker;}})();