import{_ as S,c as v,o as c,a as e,F as w,g as z,t as y,h as f,i as $,j as k,k as _,v as h,q as C,l as M,b as x,m as E,n as V,p as b}from"./index-MM3znn9C.js";const N={class:"table table-striped"},A=["onClick"],D=["onClick"],q={__name:"SystemTable",props:{systems:Array},setup(d){return(m,u)=>(c(),v("table",N,[u[0]||(u[0]=e("thead",null,[e("tr",null,[e("th",null,"#"),e("th",null,"System Name"),e("th",null,"Organization"),e("th",null,"Description"),e("th",null,"Actions")])],-1)),e("tbody",null,[(c(!0),v(w,null,z(d.systems,(a,n)=>{var i;return c(),v("tr",{key:a.id},[e("td",null,y(n+1),1),e("td",null,y(a.name),1),e("td",null,y(((i=a.organization)==null?void 0:i.name)||"N/A"),1),e("td",null,y(a.description||"N/A"),1),e("td",null,[e("button",{class:"btn btn-sm btn-warning me-2",onClick:r=>m.$emit("edit",a)},"Edit",8,A),e("button",{class:"btn btn-sm btn-danger",onClick:r=>m.$emit("delete",a.id)},"Delete",8,D)])])}),128))])]))}},B=S(q,[["__scopeId","data-v-4c9837a4"]]),I={class:"modal-overlay"},O={class:"modal-content"},U={class:"mb-3"},j={class:"mb-3"},T={class:"mb-3"},F=["value"],L={class:"d-flex justify-content-between"},P={type:"submit",class:"btn btn-primary"},G={__name:"SystemModal",props:{system:Object,organizations:Array},emits:["close","save"],setup(d,{emit:m}){const u=d,a=m,n=f({name:"",description:"",organization:null});$(()=>u.system,r=>{r?n.value={...r}:n.value={name:"",description:"",organization:null}},{immediate:!0});const i=()=>{a("save",n.value)};return(r,t)=>{var p,g;return c(),v("div",I,[e("div",O,[e("h3",null,y((p=d.system)!=null&&p.id?"Edit System":"Create System"),1),e("form",{onSubmit:k(i,["prevent"])},[e("div",U,[t[4]||(t[4]=e("label",{class:"form-label"},"System Name",-1)),_(e("input",{type:"text","onUpdate:modelValue":t[0]||(t[0]=l=>n.value.name=l),class:"form-control",required:""},null,512),[[h,n.value.name]])]),e("div",j,[t[5]||(t[5]=e("label",{class:"form-label"},"Description",-1)),_(e("textarea",{"onUpdate:modelValue":t[1]||(t[1]=l=>n.value.description=l),class:"form-control",rows:"3",required:""},null,512),[[h,n.value.description]])]),e("div",T,[t[6]||(t[6]=e("label",{class:"form-label"},"Organization",-1)),_(e("select",{"onUpdate:modelValue":t[2]||(t[2]=l=>n.value.organization=l),class:"form-control",required:""},[(c(!0),v(w,null,z(d.organizations,l=>(c(),v("option",{key:l.id,value:l.id},y(l.name),9,F))),128))],512),[[C,n.value.organization]])]),e("div",L,[e("button",{type:"button",class:"btn btn-secondary",onClick:t[3]||(t[3]=l=>r.$emit("close"))},"Cancel"),e("button",P,y((g=d.system)!=null&&g.id?"Update":"Create"),1)])],32)])])}}},H=S(G,[["__scopeId","data-v-a9e7a696"]]),J={class:"container"},K={__name:"SystemManagementView",setup(d){const m=f([]),u=f([]),a=f(!1),n=f(null),i=async()=>{var s;try{const o=await b.get("/systems/");m.value=o.data}catch(o){console.error("Error fetching systems:",o),((s=o.response)==null?void 0:s.status)===401&&(alert("Session expired. Please log in again."),window.location.href="/login")}},r=async()=>{try{const s=await b.get("/organizations/");u.value=s.data}catch(s){console.error("Error fetching organizations:",s)}},t=s=>{n.value=s?{...s}:{name:"",description:"",organization_id:null},a.value=!0},p=()=>{a.value=!1,n.value=null},g=async s=>{try{s.id?await b.put(`/systems/${s.id}/`,s):await b.post("/systems/",s),i(),p()}catch(o){console.error("Error saving system:",o)}},l=async s=>{if(confirm("Are you sure you want to delete this system?"))try{await b.delete(`/systems/${s}/`),i()}catch(o){console.error("Error deleting system:",o)}};return M(()=>{i(),r()}),(s,o)=>(c(),v("div",J,[o[1]||(o[1]=e("h2",null,"System Management",-1)),e("button",{onClick:o[0]||(o[0]=Q=>t(null)),class:"btn btn-primary mb-3"}," + Create System "),x(B,{systems:m.value,onEdit:t,onDelete:l},null,8,["systems"]),a.value?(c(),E(H,{key:0,system:n.value,organizations:u.value,onClose:p,onSave:g},null,8,["system","organizations"])):V("",!0)]))}},W=S(K,[["__scopeId","data-v-33b6f932"]]);export{W as default};
