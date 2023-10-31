/*! For license information please see 98535-olmmIvkkAos.js.LICENSE.txt */
export const id=98535;export const ids=[98535];export const modules={54040:(e,t,i)=>{var a=i(87480),o=i(79932),s=i(58417),n=i(39274);let r=class extends s.A{};r.styles=[n.W],r=(0,a.__decorate)([(0,o.Mo)("mwc-checkbox")],r)},1819:(e,t,i)=>{var a=i(87480),o=i(79932),s=i(8485),n=i(92038);let r=class extends s.a{};r.styles=[n.W],r=(0,a.__decorate)([(0,o.Mo)("mwc-formfield")],r)},39841:(e,t,i)=>{i(1449),i(65660);var a=i(9672),o=i(69491),s=i(50856),n=i(44181);(0,a.k)({_template:s.d`
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
`,is:"app-header-layout",behaviors:[n.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,o.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),i=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=i+"px"}.bind(this));var i=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(i.marginTop=t+"px",i.paddingTop=""):(i.paddingTop=t+"px",i.marginTop="")}}})},65660:(e,t,i)=>{i(1449);const a=i(50856).d`
<custom-style>
  <style is="custom-style">
    [hidden] {
      display: none !important;
    }
  </style>
</custom-style>
<custom-style>
  <style is="custom-style">
    html {

      --layout: {
        display: -ms-flexbox;
        display: -webkit-flex;
        display: flex;
      };

      --layout-inline: {
        display: -ms-inline-flexbox;
        display: -webkit-inline-flex;
        display: inline-flex;
      };

      --layout-horizontal: {
        @apply --layout;

        -ms-flex-direction: row;
        -webkit-flex-direction: row;
        flex-direction: row;
      };

      --layout-horizontal-reverse: {
        @apply --layout;

        -ms-flex-direction: row-reverse;
        -webkit-flex-direction: row-reverse;
        flex-direction: row-reverse;
      };

      --layout-vertical: {
        @apply --layout;

        -ms-flex-direction: column;
        -webkit-flex-direction: column;
        flex-direction: column;
      };

      --layout-vertical-reverse: {
        @apply --layout;

        -ms-flex-direction: column-reverse;
        -webkit-flex-direction: column-reverse;
        flex-direction: column-reverse;
      };

      --layout-wrap: {
        -ms-flex-wrap: wrap;
        -webkit-flex-wrap: wrap;
        flex-wrap: wrap;
      };

      --layout-wrap-reverse: {
        -ms-flex-wrap: wrap-reverse;
        -webkit-flex-wrap: wrap-reverse;
        flex-wrap: wrap-reverse;
      };

      --layout-flex-auto: {
        -ms-flex: 1 1 auto;
        -webkit-flex: 1 1 auto;
        flex: 1 1 auto;
      };

      --layout-flex-none: {
        -ms-flex: none;
        -webkit-flex: none;
        flex: none;
      };

      --layout-flex: {
        -ms-flex: 1 1 0.000000001px;
        -webkit-flex: 1;
        flex: 1;
        -webkit-flex-basis: 0.000000001px;
        flex-basis: 0.000000001px;
      };

      --layout-flex-2: {
        -ms-flex: 2;
        -webkit-flex: 2;
        flex: 2;
      };

      --layout-flex-3: {
        -ms-flex: 3;
        -webkit-flex: 3;
        flex: 3;
      };

      --layout-flex-4: {
        -ms-flex: 4;
        -webkit-flex: 4;
        flex: 4;
      };

      --layout-flex-5: {
        -ms-flex: 5;
        -webkit-flex: 5;
        flex: 5;
      };

      --layout-flex-6: {
        -ms-flex: 6;
        -webkit-flex: 6;
        flex: 6;
      };

      --layout-flex-7: {
        -ms-flex: 7;
        -webkit-flex: 7;
        flex: 7;
      };

      --layout-flex-8: {
        -ms-flex: 8;
        -webkit-flex: 8;
        flex: 8;
      };

      --layout-flex-9: {
        -ms-flex: 9;
        -webkit-flex: 9;
        flex: 9;
      };

      --layout-flex-10: {
        -ms-flex: 10;
        -webkit-flex: 10;
        flex: 10;
      };

      --layout-flex-11: {
        -ms-flex: 11;
        -webkit-flex: 11;
        flex: 11;
      };

      --layout-flex-12: {
        -ms-flex: 12;
        -webkit-flex: 12;
        flex: 12;
      };

      /* alignment in cross axis */

      --layout-start: {
        -ms-flex-align: start;
        -webkit-align-items: flex-start;
        align-items: flex-start;
      };

      --layout-center: {
        -ms-flex-align: center;
        -webkit-align-items: center;
        align-items: center;
      };

      --layout-end: {
        -ms-flex-align: end;
        -webkit-align-items: flex-end;
        align-items: flex-end;
      };

      --layout-baseline: {
        -ms-flex-align: baseline;
        -webkit-align-items: baseline;
        align-items: baseline;
      };

      /* alignment in main axis */

      --layout-start-justified: {
        -ms-flex-pack: start;
        -webkit-justify-content: flex-start;
        justify-content: flex-start;
      };

      --layout-center-justified: {
        -ms-flex-pack: center;
        -webkit-justify-content: center;
        justify-content: center;
      };

      --layout-end-justified: {
        -ms-flex-pack: end;
        -webkit-justify-content: flex-end;
        justify-content: flex-end;
      };

      --layout-around-justified: {
        -ms-flex-pack: distribute;
        -webkit-justify-content: space-around;
        justify-content: space-around;
      };

      --layout-justified: {
        -ms-flex-pack: justify;
        -webkit-justify-content: space-between;
        justify-content: space-between;
      };

      --layout-center-center: {
        @apply --layout-center;
        @apply --layout-center-justified;
      };

      /* self alignment */

      --layout-self-start: {
        -ms-align-self: flex-start;
        -webkit-align-self: flex-start;
        align-self: flex-start;
      };

      --layout-self-center: {
        -ms-align-self: center;
        -webkit-align-self: center;
        align-self: center;
      };

      --layout-self-end: {
        -ms-align-self: flex-end;
        -webkit-align-self: flex-end;
        align-self: flex-end;
      };

      --layout-self-stretch: {
        -ms-align-self: stretch;
        -webkit-align-self: stretch;
        align-self: stretch;
      };

      --layout-self-baseline: {
        -ms-align-self: baseline;
        -webkit-align-self: baseline;
        align-self: baseline;
      };

      /* multi-line alignment in main axis */

      --layout-start-aligned: {
        -ms-flex-line-pack: start;  /* IE10 */
        -ms-align-content: flex-start;
        -webkit-align-content: flex-start;
        align-content: flex-start;
      };

      --layout-end-aligned: {
        -ms-flex-line-pack: end;  /* IE10 */
        -ms-align-content: flex-end;
        -webkit-align-content: flex-end;
        align-content: flex-end;
      };

      --layout-center-aligned: {
        -ms-flex-line-pack: center;  /* IE10 */
        -ms-align-content: center;
        -webkit-align-content: center;
        align-content: center;
      };

      --layout-between-aligned: {
        -ms-flex-line-pack: justify;  /* IE10 */
        -ms-align-content: space-between;
        -webkit-align-content: space-between;
        align-content: space-between;
      };

      --layout-around-aligned: {
        -ms-flex-line-pack: distribute;  /* IE10 */
        -ms-align-content: space-around;
        -webkit-align-content: space-around;
        align-content: space-around;
      };

      /*******************************
                Other Layout
      *******************************/

      --layout-block: {
        display: block;
      };

      --layout-invisible: {
        visibility: hidden !important;
      };

      --layout-relative: {
        position: relative;
      };

      --layout-fit: {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-scroll: {
        -webkit-overflow-scrolling: touch;
        overflow: auto;
      };

      --layout-fullbleed: {
        margin: 0;
        height: 100vh;
      };

      /* fixed position */

      --layout-fixed-top: {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
      };

      --layout-fixed-right: {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
      };

      --layout-fixed-bottom: {
        position: fixed;
        right: 0;
        bottom: 0;
        left: 0;
      };

      --layout-fixed-left: {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
      };

    }
  </style>
</custom-style>`;a.setAttribute("style","display: none;"),document.head.appendChild(a.content);var o=document.createElement("style");o.textContent="[hidden] { display: none !important; }",document.head.appendChild(o)},14792:(e,t,i)=>{i.d(t,{J:()=>o});var a=i(47181);const o=(e,t)=>{(0,a.B)(e,"show-dialog",{dialogTag:"hui-dialog-add-media-source-ais",dialogImport:()=>Promise.all([i.e(28597),i.e(92037),i.e(70632),i.e(68200),i.e(6971),i.e(80245),i.e(854)]).then(i.bind(i,32205)),dialogParams:t})}},74053:(e,t,i)=>{i.d(t,{v:()=>o});var a=i(47181);const o=(e,t)=>{(0,a.B)(e,"show-dialog",{dialogTag:"hui-dialog-check-media-source-ais",dialogImport:()=>Promise.all([i.e(28597),i.e(92037),i.e(23823),i.e(75682)]).then(i.bind(i,83263)),dialogParams:t})}},24734:(e,t,i)=>{i.d(t,{B:()=>o});var a=i(47181);const o=(e,t)=>{(0,a.B)(e,"show-dialog",{dialogTag:"dialog-media-player-browse",dialogImport:()=>Promise.all([i.e(42850),i.e(46992),i.e(28426),i.e(63436),i.e(28597),i.e(66903),i.e(65666),i.e(50731),i.e(3762),i.e(13960),i.e(94740),i.e(58543),i.e(52154),i.e(40172),i.e(40163),i.e(3143),i.e(7083),i.e(74535),i.e(13616),i.e(49706),i.e(98002),i.e(67113)]).then(i.bind(i,52809)),dialogParams:t})}},82002:(e,t,i)=>{i.d(t,{$:()=>a});const a={title:"AI-Speaker",views:[{badges:[],cards:[{cards:[{type:"conditional",conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state_not:"Spotify"}],card:{artwork:"full-cover",entity:"media_player.wbudowany_glosnik",hide:{power:!0,runtime:!1,shuffle:!1,source:!0},icon:"mdi:monitor-speaker",more_info:!1,name:" ",shortcuts:{buttons:[{icon:"mdi:bookmark-music",id:"script.ais_add_item_to_bookmarks",type:"script"},{icon:"mdi:thumb-up",id:"script.ais_add_item_to_favorites",type:"script"}],columns:2},show_progress:!0,tts:{platform:"ais"},type:"ais-mini-media-player"}},{type:"conditional",conditions:[{entity:"sensor.ais_player_mode",state_not:"music_player"}],card:{artwork:"full-cover",entity:"media_player.wbudowany_glosnik",hide:{power:!0,runtime:!1,shuffle:!1,source:!0},icon:"mdi:monitor-speaker",more_info:!1,name:" ",shortcuts:{buttons:[{icon:"mdi:bookmark-music",id:"script.ais_add_item_to_bookmarks",type:"script"},{icon:"mdi:thumb-up",id:"script.ais_add_item_to_favorites",type:"script"}],columns:2},show_progress:!0,tts:{platform:"ais"},type:"ais-mini-media-player"}},{type:"conditional",conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],card:{artwork:"full-cover",entity:"media_player.android_tv_127_0_0_1",hide:{power:!0,runtime:!1,shuffle:!1,source:!0},icon:"mdi:monitor-speaker",more_info:!1,name:" ",type:"ais-mini-media-player"}},{type:"conditional",conditions:[{entity:"sensor.ais_gate_model",state:"AIS-PRO1"}],card:{type:"ais-expansion-panel",icon:"mdi:tune",cards:[{entities:[{entity:"input_select.ais_audio_routing"},{entity:"input_boolean.ais_audio_mono"},{entity:"input_number.media_player_speed"}],show_header_toggle:!1,type:"entities"}]}},{cards:[{cards:[{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:heart",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"ais_favorites"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ulubione"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:bookmark",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"ais_bookmarks"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"zakładki"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:monitor-speaker",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"ais_tv"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:folder",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"local_audio"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"dyski"}},type:"ais-button"}],type:"horizontal-stack"},{cards:[{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:radio",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"radio_player"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"radio"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:podcast",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"podcast_player"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"podcast"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:book-music",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"audiobooks_player"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"audiobook"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:music",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"music_player"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"muzyka"}},type:"ais-button"}],type:"horizontal-stack"}],type:"vertical-stack"},{content:"{{ states.sensor.aisknowledgeanswer.attributes.text }}\n",type:"markdown"},{card:{cards:[{cards:[{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_mode",icon:"mdi:monitor-dashboard",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"tv_on"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_on"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_mode",icon:"mdi:television-off",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"tv_off"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_off"}},type:"ais-button"}],type:"horizontal-stack"},{card:{cards:[{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_activity",icon:"mdi:youtube-tv",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"youtube"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_youtube"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_activity",icon:"mdi:spotify",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"spotify"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_spotify"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_activity",icon:"mdi:cctv",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"camera"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_cameras"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_activity",icon:"mdi:tune-variant",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"settings"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_settings"}},type:"ais-button"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_tv_mode",state:"tv_on"}],type:"conditional"},{card:{cards:[{card:{type:"glance",columns:3,show_state:!1},filter:{include:[{domain:"camera",options:{tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_show_camera",entity_id:"this.entity_id"}}}}]},type:"ais-auto-entities"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_tv_activity",state:"camera"}],type:"conditional"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"ais_tv"}],type:"conditional"},{card:{cards:[{cards:[{color:"#727272",color_type:"icon",entity:"input_select.ais_music_service",icon:"mdi:youtube",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"YouTube"}],tap_action:{action:"call-service",service:"ais_cloud.change_audio_service"},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"input_select.ais_music_service",icon:"mdi:spotify",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"Spotify"}],tap_action:{action:"call-service",service:"ais_cloud.change_audio_service"},type:"ais-button"}],type:"horizontal-stack"},{card:{cards:[{entities:[{entity:"input_text.ais_music_query"}],show_header_toggle:!1,title:"Wyszukiwanie Muzyki",type:"entities"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"YouTube"}],type:"conditional"},{card:{cards:[{entities:[{entity:"input_text.ais_spotify_query"}],show_header_toggle:!1,title:"Wyszukiwanie Muzyki",type:"entities"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],type:"conditional"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"}],type:"conditional"},{cards:[{type:"ais-auto-entities",card:{type:"vertical-stack"},card_param:"cards",filter:{exclude:[{entity_id:"media_player.wbudowany_glosnik"}],include:[{domain:"media_player",options:{type:"custom:hui-ais-mini-media-player-card",artwork:"cover-fit",source:"full"}}]}}],icon:"mdi:speaker-multiple",type:"ais-expansion-panel"},{card:{cards:[{entity:"input_select.book_autor",type:"ais-easy-picker"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"audiobooks_player"}],type:"conditional"}],show_header_toggle:!1,type:"vertical-stack"},{cards:[{card:{entity:"sensor.ais_drives",title:"Przeglądanie Dysków",type:"ais-files-list"},conditions:[{entity:"sensor.ais_player_mode",state:"local_audio"}],type:"conditional"},{card:{entity:["sensor.aisbookmarkslist"],media_source:"Bookmark",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"ais_bookmarks"}],type:"conditional"},{card:{entity:["sensor.aisfavoriteslist"],media_source:"Favorite",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"ais_favorites"}],type:"conditional"},{card:{entity:["sensor.youtubelist"],media_source:"Music",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"YouTube"}],type:"conditional"},{card:{cards:[{icon:"mdi:folder-music",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"featured-playlists"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"featured-playlists"}},type:"ais-button"},{icon:"mdi:playlist-music",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"playlists"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"playlists"}},type:"ais-button"},{icon:"mdi:account",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"artists"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"artists"}},type:"ais-button"},{icon:"mdi:album",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"albums"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"albums"}},type:"ais-button"},{icon:"mdi:music-note",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"tracks"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"tracks"}},type:"ais-button"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],type:"conditional"},{card:{entity:["sensor.spotifysearchlist"],media_source:"SpotifySearch",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],type:"conditional"},{card:{cards:[{icon:"mdi:account",entity:"sensor.ais_radio_origin",show_name:!0,name:"Moje",state:[{color:"var(--primary-color)",value:"private"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"radio_private"}},type:"ais-button"},{icon:"mdi:earth",entity:"sensor.ais_radio_origin",show_name:!0,name:"Publiczne",state:[{color:"var(--primary-color)",value:"public"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"radio_public"}},type:"ais-button"},{icon:"mdi:share-variant",entity:"sensor.ais_radio_origin",show_name:!0,name:"Udostępnione",state:[{color:"var(--primary-color)",value:"shared"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"radio_shared"}},type:"ais-button"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"}],type:"conditional"},{card:{entity:"input_select.radio_type",type:"ais-easy-picker",orgin:"public"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"},{entity:"sensor.ais_radio_origin",state:"public"}],type:"conditional"},{card:{entity:"input_select.radio_type",type:"ais-easy-picker",orgin:"private"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"},{entity:"sensor.ais_radio_origin",state:"private"}],type:"conditional"},{card:{entity:"input_select.radio_type",type:"ais-easy-picker",orgin:"shared"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"},{entity:"sensor.ais_radio_origin",state:"shared"}],type:"conditional"},{card:{cards:[{icon:"mdi:account",entity:"sensor.ais_podcast_origin",show_name:!0,name:"Moje",state:[{color:"var(--primary-color)",value:"private"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"podcast_private"}},type:"ais-button"},{icon:"mdi:earth",entity:"sensor.ais_podcast_origin",show_name:!0,name:"Publiczne",state:[{color:"var(--primary-color)",value:"public"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"podcast_public"}},type:"ais-button"},{icon:"mdi:share-variant",entity:"sensor.ais_podcast_origin",show_name:!0,name:"Udostępnione",state:[{color:"var(--primary-color)",value:"shared"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"podcast_shared"}},type:"ais-button"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"}],type:"conditional"},{card:{entity:"input_select.podcast_type",type:"ais-easy-picker",orgin:"public"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"},{entity:"sensor.ais_podcast_origin",state:"public"}],type:"conditional"},{card:{entity:"input_select.podcast_type",type:"ais-easy-picker",orgin:"private"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"},{entity:"sensor.ais_podcast_origin",state:"private"}],type:"conditional"},{card:{entity:"input_select.podcast_type",type:"ais-easy-picker",orgin:"shared"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"},{entity:"sensor.ais_podcast_origin",state:"shared"}],type:"conditional"},{card:{entity:["sensor.podcastnamelist"],media_source:"PodcastName",type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"}],type:"conditional"},{card:{entity:["sensor.audiobookslist"],media_source:"AudioBook",type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"audiobooks_player"}],type:"conditional"}],type:"vertical-stack"},{cards:[{card:{entity:["sensor.spotifylist"],media_source:"Spotify",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],type:"conditional"},{card:{entity:["sensor.radiolist"],media_source:"Radio",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"}],type:"conditional"},{card:{entity:["sensor.podcastlist"],media_source:"Podcast",type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"}],type:"conditional"},{card:{entity:["sensor.audiobookschapterslist"],media_source:"AudioBookChapter",type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"audiobooks_player"}],type:"conditional"}],type:"vertical-stack"}],icon:"mdi:music",path:"aisaudio",title:"Audio",visible:!1}]}},98535:(e,t,i)=>{i.a(e,(async(e,a)=>{try{i.r(t);var o=i(17463),s=i(68144),n=i(79932),r=(i(39841),i(27289),i(12730),i(54040),i(1819),i(51444)),l=i(24734),c=i(74053),d=i(14792),p=(i(48932),i(22098),i(82002)),y=i(10009),_=i(11654),u=e([y]);y=(u.then?(await u)():u)[0];const m="M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z",v="M22,4H14L12,2H6A2,2 0 0,0 4,4V16A2,2 0 0,0 6,18H22A2,2 0 0,0 24,16V6A2,2 0 0,0 22,4M2,6H0V11H0V20A2,2 0 0,0 2,22H20V20H2V6Z",f="M17 9V12H14V14H17V17H19V14H22V12H19V9H17M9 3V13.55C8.41 13.21 7.73 13 7 13C4.79 13 3 14.79 3 17S4.79 21 7 21 11 19.21 11 17V7H15V3H9Z",h="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z";(0,o.Z)([(0,n.Mo)("ha-panel-aisaudio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"method",key:"_showBrowseMedia",value:function(){(0,l.B)(this,{action:"play",entityId:"media_player.wbudowany_glosnik",mediaPickedCallback:e=>this.hass.callService("media_player","play_media",{entity_id:"media_player.wbudowany_glosnik",media_content_id:e.item.media_content_id,media_content_type:e.item.media_content_type})})}},{kind:"method",key:"_showCheckAisMedia",value:function(){(0,c.v)(this,{selectedOptionCallback:e=>console.log("option: "+e)})}},{kind:"method",key:"_showAddAisMedia",value:function(){(0,d.J)(this,{selectedOptionCallback:e=>console.log("option: "+e)})}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,r._)(this,this.hass,{pipeline_id:"last_used"})}},{kind:"method",key:"render",value:function(){const e={config:p.$,rawConfig:p.$,editMode:!1,urlPath:null,enableFullEditMode:()=>{},mode:"storage",locale:this.hass.locale,saveConfig:async()=>{},deleteConfig:async()=>{},setEditMode:()=>{}};return s.dy` <app-header-layout has-scrolling-region> <app-header fixed slot="header"> <app-toolbar> <ha-menu-button .hass="${this.hass}" .narrow="${this.narrow}"></ha-menu-button> <ha-icon-button label="Informacje o audio" .path="${h}" @click="${this._showCheckAisMedia}"></ha-icon-button> <ha-icon-button label="Dodaj audio" icon="hass:music-note-plus" .path="${f}" @click="${this._showAddAisMedia}"></ha-icon-button> <div main-title>Audio</div> <ha-icon-button label="Przeglądaj media" .path="${v}" @click="${this._showBrowseMedia}"></ha-icon-button> <ha-icon-button label="Rozpocznij rozmowę" .path="${m}" @click="${this._showVoiceCommandDialog}"></ha-icon-button> </app-toolbar> </app-header> <hui-view .hass="${this.hass}" .lovelace="${e}" index="0"></hui-view> </app-header-layout> `}},{kind:"get",static:!0,key:"styles",value:function(){return[_.Qx,s.iv`:host{min-height:100vh;height:0;display:flex;flex-direction:column;box-sizing:border-box;background:var(--primary-background-color)}:host>*{flex:1}`]}}]}}),s.oi);a()}catch(e){a(e)}}))}};
//# sourceMappingURL=98535-olmmIvkkAos.js.map