/*! For license information please see 84487-xgdOggmmD1E.js.LICENSE.txt */
export const id=84487;export const ids=[84487];export const modules={53464:(e,t,r)=>{r.d(t,{H:()=>b});var i=r(87480),o=(r(27763),r(38103)),n=r(78220),a=r(14114),s=r(98734),c=r(72774),l={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},d={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const h=function(e){function t(r){return e.call(this,(0,i.__assign)((0,i.__assign)({},t.defaultAdapter),r))||this}return(0,i.__extends)(t,e),Object.defineProperty(t,"strings",{get:function(){return d},enumerable:!1,configurable:!0}),Object.defineProperty(t,"cssClasses",{get:function(){return l},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),t.prototype.setChecked=function(e){this.adapter.setNativeControlChecked(e),this.updateAriaChecked(e),this.updateCheckedStyling(e)},t.prototype.setDisabled=function(e){this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(l.DISABLED):this.adapter.removeClass(l.DISABLED)},t.prototype.handleChange=function(e){var t=e.target;this.updateAriaChecked(t.checked),this.updateCheckedStyling(t.checked)},t.prototype.updateCheckedStyling=function(e){e?this.adapter.addClass(l.CHECKED):this.adapter.removeClass(l.CHECKED)},t.prototype.updateAriaChecked=function(e){this.adapter.setNativeControlAttr(d.ARIA_CHECKED_ATTR,""+!!e)},t}(c.K);var p=r(68144),u=r(79932),m=r(30153);class b extends n.H{constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=h,this.rippleHandlers=new s.A((()=>(this.shouldRenderRipple=!0,this.ripple)))}changeHandler(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,n.q)(this.mdcRoot)),{setNativeControlChecked:e=>{this.formElement.checked=e},setNativeControlDisabled:e=>{this.formElement.disabled=e},setNativeControlAttr:(e,t)=>{this.formElement.setAttribute(e,t)}})}renderRipple(){return this.shouldRenderRipple?p.dy` <mwc-ripple .accent="${this.checked}" .disabled="${this.disabled}" unbounded> </mwc-ripple>`:""}focus(){const e=this.formElement;e&&(this.rippleHandlers.startFocus(),e.focus())}blur(){const e=this.formElement;e&&(this.rippleHandlers.endFocus(),e.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}render(){return p.dy` <div class="mdc-switch"> <div class="mdc-switch__track"></div> <div class="mdc-switch__thumb-underlay"> ${this.renderRipple()} <div class="mdc-switch__thumb"> <input type="checkbox" id="basic-switch" class="mdc-switch__native-control" role="switch" aria-label="${(0,m.o)(this.ariaLabel)}" aria-labelledby="${(0,m.o)(this.ariaLabelledBy)}" @change="${this.changeHandler}" @focus="${this.handleRippleFocus}" @blur="${this.handleRippleBlur}" @mousedown="${this.handleRippleMouseDown}" @mouseenter="${this.handleRippleMouseEnter}" @mouseleave="${this.handleRippleMouseLeave}" @touchstart="${this.handleRippleTouchStart}" @touchend="${this.handleRippleDeactivate}" @touchcancel="${this.handleRippleDeactivate}"> </div> </div> </div>`}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}}(0,i.__decorate)([(0,u.Cb)({type:Boolean}),(0,a.P)((function(e){this.mdcFoundation.setChecked(e)}))],b.prototype,"checked",void 0),(0,i.__decorate)([(0,u.Cb)({type:Boolean}),(0,a.P)((function(e){this.mdcFoundation.setDisabled(e)}))],b.prototype,"disabled",void 0),(0,i.__decorate)([o.L,(0,u.Cb)({attribute:"aria-label"})],b.prototype,"ariaLabel",void 0),(0,i.__decorate)([o.L,(0,u.Cb)({attribute:"aria-labelledby"})],b.prototype,"ariaLabelledBy",void 0),(0,i.__decorate)([(0,u.IO)(".mdc-switch")],b.prototype,"mdcRoot",void 0),(0,i.__decorate)([(0,u.IO)("input")],b.prototype,"formElement",void 0),(0,i.__decorate)([(0,u.GC)("mwc-ripple")],b.prototype,"ripple",void 0),(0,i.__decorate)([(0,u.SB)()],b.prototype,"shouldRenderRipple",void 0),(0,i.__decorate)([(0,u.hO)({passive:!0})],b.prototype,"handleRippleMouseDown",null),(0,i.__decorate)([(0,u.hO)({passive:!0})],b.prototype,"handleRippleTouchStart",null)},4301:(e,t,r)=>{r.d(t,{W:()=>i});const i=r(68144).iv`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}.mdc-switch__thumb-underlay[dir=rtl],[dir=rtl] .mdc-switch__thumb-underlay{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:0;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary,#018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary,#018786);border-color:#018786;border-color:var(--mdc-theme-secondary,#018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface,#000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface,#fff);border-color:#fff;border-color:var(--mdc-theme-surface,#fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(.4,0,.2,1)}.mdc-switch__native-control[dir=rtl],[dir=rtl] .mdc-switch__native-control{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(.4,0,.2,1),background-color 90ms cubic-bezier(.4,0,.2,1),border-color 90ms cubic-bezier(.4,0,.2,1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(.4,0,.2,1),background-color 90ms cubic-bezier(.4,0,.2,1),border-color 90ms cubic-bezier(.4,0,.2,1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0,0,0,.2),0px 2px 2px 0px rgba(0,0,0,.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl],[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control[dir=rtl],[dir=rtl] .mdc-switch--checked .mdc-switch__native-control{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:0;-webkit-tap-highlight-color:transparent}`},39841:(e,t,r)=>{r(1449),r(65660);var i=r(9672),o=r(69491),n=r(50856),a=r(44181);(0,i.k)({_template:n.d`
    <style>
      :host {
        display: block;
        /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
        position: relative;
        z-index: 0;
      }

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) #wrapper #contentContainer {
        @apply --layout-fit;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
        position: relative;
      }

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[a.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,o.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),r=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=r+"px"}.bind(this));var r=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(r.marginTop=t+"px",r.paddingTop=""):(r.paddingTop=t+"px",r.marginTop="")}}})},53973:(e,t,r)=>{r(1449),r(65660),r(97968);var i=r(9672),o=r(50856),n=r(33760);(0,i.k)({_template:o.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[n.U]})},55020:(e,t,r)=>{r.d(t,{j:()=>o});var i={};function o(){return i}},5763:(e,t,r)=>{function i(e){var t=new Date(Date.UTC(e.getFullYear(),e.getMonth(),e.getDate(),e.getHours(),e.getMinutes(),e.getSeconds(),e.getMilliseconds()));return t.setUTCFullYear(e.getFullYear()),e.getTime()-t.getTime()}r.d(t,{Z:()=>i})},23682:(e,t,r)=>{function i(e,t){if(t.length<e)throw new TypeError(e+" argument"+(e>1?"s":"")+" required, but only "+t.length+" present")}r.d(t,{Z:()=>i})},86102:(e,t,r)=>{r.d(t,{u:()=>n});var i={ceil:Math.ceil,round:Math.round,floor:Math.floor,trunc:function(e){return e<0?Math.ceil(e):Math.floor(e)}},o="trunc";function n(e){return e?i[e]:i[o]}},90394:(e,t,r)=>{function i(e){if(null===e||!0===e||!1===e)return NaN;var t=Number(e);return isNaN(t)?t:t<0?Math.ceil(t):Math.floor(t)}r.d(t,{Z:()=>i})},24112:(e,t,r)=>{r.d(t,{Z:()=>l});var i=r(34327),o=r(5763),n=r(59429),a=r(23682),s=864e5;function c(e,t){var r=e.getFullYear()-t.getFullYear()||e.getMonth()-t.getMonth()||e.getDate()-t.getDate()||e.getHours()-t.getHours()||e.getMinutes()-t.getMinutes()||e.getSeconds()-t.getSeconds()||e.getMilliseconds()-t.getMilliseconds();return r<0?-1:r>0?1:r}function l(e,t){(0,a.Z)(2,arguments);var r=(0,i.Z)(e),l=(0,i.Z)(t),d=c(r,l),h=Math.abs(function(e,t){(0,a.Z)(2,arguments);var r=(0,n.Z)(e),i=(0,n.Z)(t),c=r.getTime()-(0,o.Z)(r),l=i.getTime()-(0,o.Z)(i);return Math.round((c-l)/s)}(r,l));r.setDate(r.getDate()-d*h);var p=d*(h-Number(c(r,l)===-d));return 0===p?0:p}},35040:(e,t,r)=>{r.d(t,{Z:()=>a});var i=r(24112),o=r(23682),n=r(86102);function a(e,t,r){(0,o.Z)(2,arguments);var a=(0,i.Z)(e,t)/7;return(0,n.u)(null==r?void 0:r.roundingMethod)(a)}},59429:(e,t,r)=>{r.d(t,{Z:()=>n});var i=r(34327),o=r(23682);function n(e){(0,o.Z)(1,arguments);var t=(0,i.Z)(e);return t.setHours(0,0,0,0),t}},59401:(e,t,r)=>{r.d(t,{Z:()=>s});var i=r(34327),o=r(90394),n=r(23682),a=r(55020);function s(e,t){var r,s,c,l,d,h,p,u;(0,n.Z)(1,arguments);var m=(0,a.j)(),b=(0,o.Z)(null!==(r=null!==(s=null!==(c=null!==(l=null==t?void 0:t.weekStartsOn)&&void 0!==l?l:null==t||null===(d=t.locale)||void 0===d||null===(h=d.options)||void 0===h?void 0:h.weekStartsOn)&&void 0!==c?c:m.weekStartsOn)&&void 0!==s?s:null===(p=m.locale)||void 0===p||null===(u=p.options)||void 0===u?void 0:u.weekStartsOn)&&void 0!==r?r:0);if(!(b>=0&&b<=6))throw new RangeError("weekStartsOn must be between 0 and 6 inclusively");var g=(0,i.Z)(e),v=g.getDay(),f=(v<b?7:0)+v-b;return g.setDate(g.getDate()-f),g.setHours(0,0,0,0),g}},34327:(e,t,r)=>{r.d(t,{Z:()=>n});var i=r(76775),o=r(23682);function n(e){(0,o.Z)(1,arguments);var t=Object.prototype.toString.call(e);return e instanceof Date||"object"===(0,i.Z)(e)&&"[object Date]"===t?new Date(e.getTime()):"number"==typeof e||"[object Number]"===t?new Date(e):("string"!=typeof e&&"[object String]"!==t||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://github.com/date-fns/date-fns/blob/master/docs/upgradeGuide.md#string-arguments"),console.warn((new Error).stack)),new Date(NaN))}},22075:(e,t,r)=>{r.d(t,{L:()=>n});const i={en:"US",hi:"IN",deva:"IN",te:"IN",mr:"IN",ta:"IN",gu:"IN",kn:"IN",or:"IN",ml:"IN",pa:"IN",bho:"IN",awa:"IN",as:"IN",mwr:"IN",mai:"IN",mag:"IN",bgc:"IN",hne:"IN",dcc:"IN",bn:"BD",beng:"BD",rkt:"BD",dz:"BT",tibt:"BT",tn:"BW",am:"ET",ethi:"ET",om:"ET",quc:"GT",id:"ID",jv:"ID",su:"ID",mad:"ID",ms_arab:"ID",he:"IL",hebr:"IL",jam:"JM",ja:"JP",jpan:"JP",km:"KH",khmr:"KH",ko:"KR",kore:"KR",lo:"LA",laoo:"LA",mh:"MH",my:"MM",mymr:"MM",mt:"MT",ne:"NP",fil:"PH",ceb:"PH",ilo:"PH",ur:"PK",pa_arab:"PK",lah:"PK",ps:"PK",sd:"PK",skr:"PK",gn:"PY",th:"TH",thai:"TH",tts:"TH",zh_hant:"TW",hant:"TW",sm:"WS",zu:"ZA",sn:"ZW",arq:"DZ",ar:"EG",arab:"EG",arz:"EG",fa:"IR",az_arab:"IR",dv:"MV",thaa:"MV"};const o={AG:0,ATG:0,28:0,AS:0,ASM:0,16:0,BD:0,BGD:0,50:0,BR:0,BRA:0,76:0,BS:0,BHS:0,44:0,BT:0,BTN:0,64:0,BW:0,BWA:0,72:0,BZ:0,BLZ:0,84:0,CA:0,CAN:0,124:0,CO:0,COL:0,170:0,DM:0,DMA:0,212:0,DO:0,DOM:0,214:0,ET:0,ETH:0,231:0,GT:0,GTM:0,320:0,GU:0,GUM:0,316:0,HK:0,HKG:0,344:0,HN:0,HND:0,340:0,ID:0,IDN:0,360:0,IL:0,ISR:0,376:0,IN:0,IND:0,356:0,JM:0,JAM:0,388:0,JP:0,JPN:0,392:0,KE:0,KEN:0,404:0,KH:0,KHM:0,116:0,KR:0,KOR:0,410:0,LA:0,LA0:0,418:0,MH:0,MHL:0,584:0,MM:0,MMR:0,104:0,MO:0,MAC:0,446:0,MT:0,MLT:0,470:0,MX:0,MEX:0,484:0,MZ:0,MOZ:0,508:0,NI:0,NIC:0,558:0,NP:0,NPL:0,524:0,PA:0,PAN:0,591:0,PE:0,PER:0,604:0,PH:0,PHL:0,608:0,PK:0,PAK:0,586:0,PR:0,PRI:0,630:0,PT:0,PRT:0,620:0,PY:0,PRY:0,600:0,SA:0,SAU:0,682:0,SG:0,SGP:0,702:0,SV:0,SLV:0,222:0,TH:0,THA:0,764:0,TT:0,TTO:0,780:0,TW:0,TWN:0,158:0,UM:0,UMI:0,581:0,US:0,USA:0,840:0,VE:0,VEN:0,862:0,VI:0,VIR:0,850:0,WS:0,WSM:0,882:0,YE:0,YEM:0,887:0,ZA:0,ZAF:0,710:0,ZW:0,ZWE:0,716:0,AE:6,ARE:6,784:6,AF:6,AFG:6,4:6,BH:6,BHR:6,48:6,DJ:6,DJI:6,262:6,DZ:6,DZA:6,12:6,EG:6,EGY:6,818:6,IQ:6,IRQ:6,368:6,IR:6,IRN:6,364:6,JO:6,JOR:6,400:6,KW:6,KWT:6,414:6,LY:6,LBY:6,434:6,OM:6,OMN:6,512:6,QA:6,QAT:6,634:6,SD:6,SDN:6,729:6,SY:6,SYR:6,760:6,MV:5,MDV:5,462:5};function n(e){return function(e,t,r){if(e){var i,o=e.toLowerCase().split(/[-_]/),n=o[0],a=n;if(o[1]&&4===o[1].length?(a+="_"+o[1],i=o[2]):i=o[1],i||(i=t[a]||t[n]),i)return function(e,t){var r=t["string"==typeof e?e.toUpperCase():e];return"number"==typeof r?r:1}(i.match(/^\d+$/)?Number(i):i,r)}return 1}(e,i,o)}},82160:(e,t,r)=>{function i(e){return new Promise(((t,r)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>r(e.error)}))}function o(e,t){const r=indexedDB.open(e);r.onupgradeneeded=()=>r.result.createObjectStore(t);const o=i(r);return(e,r)=>o.then((i=>r(i.transaction(t,e).objectStore(t))))}let n;function a(){return n||(n=o("keyval-store","keyval")),n}function s(e,t=a()){return t("readonly",(t=>i(t.get(e))))}function c(e,t,r=a()){return r("readwrite",(r=>(r.put(t,e),i(r.transaction))))}function l(e=a()){return e("readwrite",(e=>(e.clear(),i(e.transaction))))}r.d(t,{MT:()=>o,RV:()=>i,U2:()=>s,ZH:()=>l,t8:()=>c})},57835:(e,t,r)=>{r.d(t,{XM:()=>i.XM,Xe:()=>i.Xe,pX:()=>i.pX});var i=r(38941)}};
//# sourceMappingURL=84487-xgdOggmmD1E.js.map