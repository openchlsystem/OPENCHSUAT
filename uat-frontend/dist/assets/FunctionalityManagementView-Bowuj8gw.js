import{_ as b,c,o as r,a as t,F as M,g as _,t as d,h as g,i as $,j as C,k as p,v,q as k,r as F,b as w,m as E,n as S,p as u}from"./index-C7sBCj21.js";const x={props:{functionalities:Array}},D={class:"d-flex justify-content-between align-items-center mb-3"},V={class:"table table-striped"},A=["onClick"],N=["onClick"];function T(e,s,m,f,i,a){return r(),c("div",null,[t("div",D,[s[1]||(s[1]=t("h3",null,"Functionalities",-1)),t("button",{onClick:s[0]||(s[0]=o=>e.$emit("openModal")),class:"btn btn-primary"},"+ Add Functionality")]),t("table",V,[s[2]||(s[2]=t("thead",{class:"table-dark"},[t("tr",null,[t("th",null,"Name"),t("th",null,"System"),t("th",null,"Description"),t("th",null,"Actions")])],-1)),t("tbody",null,[(r(!0),c(M,null,_(m.functionalities,o=>{var n;return r(),c("tr",{key:o.id},[t("td",null,d(o.name),1),t("td",null,d(((n=o.system)==null?void 0:n.name)||"N/A"),1),t("td",null,d(o.description),1),t("td",null,[t("button",{onClick:y=>e.$emit("edit",o),class:"btn btn-warning btn-sm"},"Edit",8,A),t("button",{onClick:y=>e.$emit("delete",o.id),class:"btn btn-danger btn-sm"},"Delete",8,N)])])}),128))])])])}const U=b(x,[["render",T]]),j={class:"modal-overlay"},q={class:"modal-content"},B={class:"mb-3"},O={class:"mb-3"},I={class:"mb-3"},L=["value"],z={class:"d-flex justify-content-between"},G={type:"submit",class:"btn btn-primary"},H={__name:"FunctionalityModal",props:{functionality:Object,systems:Array},emits:["close","save"],setup(e,{emit:s}){const m=e,f=s,i=g({name:"",description:"",system:null});$(()=>m.functionality,o=>{var n;o?i.value={id:o.id||null,name:o.name||"",description:o.description||"",system:((n=o.system)==null?void 0:n.id)||null}:i.value={name:"",description:"",system:null}},{immediate:!0});const a=()=>{f("save",{...i.value})};return(o,n)=>{var y,h;return r(),c("div",j,[t("div",q,[t("h3",null,d((y=e.functionality)!=null&&y.id?"Edit Functionality":"Create Functionality"),1),t("form",{onSubmit:C(a,["prevent"])},[t("div",B,[n[4]||(n[4]=t("label",{class:"form-label"},"Functionality Name",-1)),p(t("input",{type:"text","onUpdate:modelValue":n[0]||(n[0]=l=>i.value.name=l),class:"form-control",required:""},null,512),[[v,i.value.name]])]),t("div",O,[n[5]||(n[5]=t("label",{class:"form-label"},"Description",-1)),p(t("textarea",{"onUpdate:modelValue":n[1]||(n[1]=l=>i.value.description=l),class:"form-control",rows:"3",required:""},null,512),[[v,i.value.description]])]),t("div",I,[n[6]||(n[6]=t("label",{class:"form-label"},"System",-1)),p(t("select",{"onUpdate:modelValue":n[2]||(n[2]=l=>i.value.system=l),class:"form-control",required:""},[(r(!0),c(M,null,_(e.systems,l=>(r(),c("option",{key:l.id,value:l.id},d(l.name),9,L))),128))],512),[[k,i.value.system]])]),t("div",z,[t("button",{type:"button",class:"btn btn-secondary",onClick:n[3]||(n[3]=l=>o.$emit("close"))},"Cancel"),t("button",G,d((h=e.functionality)!=null&&h.id?"Update":"Create"),1)])],32)])])}}},J=b(H,[["__scopeId","data-v-9f619714"]]),K={components:{FunctionalityTable:U,FunctionalityModal:J},data(){return{functionalities:[],systems:[],showModal:!1,selectedFunctionality:null}},methods:{async fetchFunctionalities(){try{const e=await u.get("/functionalities/");this.functionalities=e.data}catch(e){console.error("Error fetching functionalities:",e)}},async fetchSystems(){try{const e=await u.get("/systems/");this.systems=e.data}catch(e){console.error("Error fetching systems:",e)}},openCreateModal(){console.log("✅ Opening Create Modal"),this.selectedFunctionality={id:null,name:"",description:"",system:null},this.showModal=!0,this.$nextTick(()=>this.$forceUpdate())},editFunctionality(e){console.log("✅ Editing Functionality",e),this.selectedFunctionality={...e},this.showModal=!0},async deleteFunctionality(e){if(confirm("Are you sure you want to delete this functionality?"))try{await u.delete(`/functionalities/${e}/`),this.functionalities=this.functionalities.filter(s=>s.id!==e)}catch(s){console.error("Error deleting functionality:",s)}},async saveFunctionality(e){try{e.id?await u.put(`/functionalities/${e.id}/`,e):await u.post("/functionalities/",e),this.fetchFunctionalities(),this.closeModal()}catch(s){console.error("Error saving functionality:",s)}},closeModal(){console.log("✅ Closing Modal"),this.selectedFunctionality=null,this.showModal=!1}},mounted(){this.fetchFunctionalities(),this.fetchSystems()}},P={class:"container mt-4"};function Q(e,s,m,f,i,a){const o=F("FunctionalityTable"),n=F("FunctionalityModal");return r(),c("div",P,[s[0]||(s[0]=t("h2",{class:"mb-4"},"Functionality Management",-1)),w(o,{functionalities:i.functionalities,onOpenModal:a.openCreateModal,onEdit:a.editFunctionality,onDelete:a.deleteFunctionality},null,8,["functionalities","onOpenModal","onEdit","onDelete"]),i.showModal?(r(),E(n,{key:0,functionality:i.selectedFunctionality,systems:i.systems,onClose:a.closeModal,onSave:a.saveFunctionality},null,8,["functionality","systems","onClose","onSave"])):S("",!0)])}const W=b(K,[["render",Q]]);export{W as default};
