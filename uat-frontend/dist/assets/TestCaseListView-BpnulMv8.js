import{_ as S,c as r,o as i,a as t,F as y,g as M,t as u,s as U,p,j as v,k as h,v as T,x as E,r as f,m as C,n as b,q as $,b as N}from"./index-C7sBCj21.js";const V={props:{testCases:Array}},I={class:"test-case-table"},F={class:"table-header"},D={class:"table table-hover"},q=["onClick"],O={class:"action-buttons"},R=["onClick"],j=["onClick"],B=["onClick"],z=["onClick"];function L(s,e,d,_,l,n){return i(),r("div",I,[t("div",F,[e[1]||(e[1]=t("h3",null,"📝 Test Cases",-1)),t("button",{onClick:e[0]||(e[0]=o=>s.$emit("openModal")),class:"btn btn-primary"},"+ Add Test Case")]),t("table",D,[e[2]||(e[2]=t("thead",{class:"table-dark"},[t("tr",null,[t("th",null,"Title"),t("th",null,"Functionality"),t("th",null,"Expected Result"),t("th",null,"Created By"),t("th",null,"Status"),t("th",null,"Actions")])],-1)),t("tbody",null,[(i(!0),r(y,null,M(d.testCases,o=>{var a,c;return i(),r("tr",{key:o.id},[t("td",null,u(o.title),1),t("td",null,u(o.functionalityName||"N/A"),1),t("td",null,u(o.expected_result),1),t("td",null,u(((a=o.created_by)==null?void 0:a.first_name)||((c=o.created_by)==null?void 0:c.whatsapp_number)||"N/A"),1),t("td",null,[t("button",{class:U(["btn status-btn",o.assigned_user?"btn-success":"btn-secondary"]),onClick:m=>s.$emit("assign",o)},u(o.assigned_user?"Assigned":"Not Assigned"),11,q)]),t("td",null,[t("div",O,[t("button",{onClick:m=>s.$emit("edit",o),class:"btn btn-warning"},"✏️ Edit",8,R),t("button",{onClick:m=>s.$emit("delete",o.id),class:"btn btn-danger"},"🗑 Delete",8,j),t("button",{onClick:m=>s.$emit("viewSteps",o),class:"btn btn-info"},"📜 View Steps",8,B),t("button",{onClick:m=>s.$emit("addStep",o),class:"btn btn-info"},"➕ Add Step",8,z)])])])}),128))])])])}const W=S(V,[["render",L],["__scopeId","data-v-cf1e16b5"]]),P={props:{testCaseId:{type:Number,required:!0},stepToEdit:{type:Object,default:null}},data(){return{step:{step_number:1,description:"",expected_result:"",attachment:null},file:null}},watch:{stepToEdit:{immediate:!0,handler(s){s?this.step={...s}:this.resetForm()}}},methods:{resetForm(){this.step={step_number:1,description:"",expected_result:"",attachment:null},this.file=null},handleFileUpload(s){this.file=s.target.files[0]},async saveStep(){try{const s=new FormData;s.append("step_number",this.step.step_number),s.append("description",this.step.description),s.append("expected_result",this.step.expected_result),s.append("test_case",this.testCaseId),this.file&&s.append("attachment",this.file),this.stepToEdit?await p.put(`/test-steps/${this.stepToEdit.id}/`,s,{headers:{"Content-Type":"multipart/form-data"}}):await p.post("/test-steps/",s,{headers:{"Content-Type":"multipart/form-data"}}),this.$emit("saved"),this.closeModal()}catch(s){console.error("Error saving test step:",s),this.$emit("error",s)}},closeModal(){this.$emit("close")}}},G={class:"modal-overlay"},H={class:"modal-content"},J={class:"modal-title"},K={class:"form-group"},Q={class:"form-group"},X={class:"form-group"},Y={class:"form-group"},Z={class:"form-group"},ee={type:"submit",class:"btn btn-primary"};function te(s,e,d,_,l,n){return i(),r("div",G,[t("div",H,[t("h3",J,u(d.stepToEdit?"Edit Step":"Add Step"),1),t("form",{onSubmit:e[5]||(e[5]=v((...o)=>n.saveStep&&n.saveStep(...o),["prevent"]))},[t("div",K,[e[6]||(e[6]=t("label",{for:"stepNumber"},"Step Number",-1)),h(t("input",{type:"number",id:"stepNumber","onUpdate:modelValue":e[0]||(e[0]=o=>l.step.step_number=o),class:"form-control",required:""},null,512),[[T,l.step.step_number]])]),t("div",Q,[e[7]||(e[7]=t("label",{for:"description"},"Description",-1)),h(t("textarea",{id:"description","onUpdate:modelValue":e[1]||(e[1]=o=>l.step.description=o),class:"form-control",required:""},null,512),[[T,l.step.description]])]),t("div",X,[e[8]||(e[8]=t("label",{for:"expectedResult"},"Expected Result",-1)),h(t("textarea",{id:"expectedResult","onUpdate:modelValue":e[2]||(e[2]=o=>l.step.expected_result=o),class:"form-control",required:""},null,512),[[T,l.step.expected_result]])]),t("div",Y,[e[9]||(e[9]=t("label",{for:"attachment"},"Attachment",-1)),t("input",{type:"file",id:"attachment",onChange:e[3]||(e[3]=(...o)=>n.handleFileUpload&&n.handleFileUpload(...o)),class:"form-control"},null,32)]),t("div",Z,[t("button",ee,u(d.stepToEdit?"Update":"Save"),1),t("button",{type:"button",onClick:e[4]||(e[4]=(...o)=>n.closeModal&&n.closeModal(...o)),class:"btn btn-secondary"}," Cancel ")])],32)])])}const A=S(P,[["render",te],["__scopeId","data-v-ad780708"]]),se=E(),oe={components:{AddTestStepModal:A},props:{testCase:Object,functionalities:{type:Array,default:()=>[]}},data(){return{localTestCase:{},showAddStepModal:!1}},watch:{testCase:{immediate:!0,handler(s){this.localTestCase=s?{...s}:{title:"",functionality:"",description:"",expected_result:""}}}},methods:{save(){this.$emit("save",this.localTestCase)},openAddStepModal(){if(!this.localTestCase.id){se.warning("Please save the test case before adding steps.");return}this.showAddStepModal=!0},closeAddStepModal(){this.showAddStepModal=!1},handleStepSaved(){this.closeAddStepModal(),this.$emit("step-saved")}}},ne={class:"modal-content"},le={key:0},ae={key:1},ie={class:"form-group"},de={class:"form-group"},re=["value"],ce={class:"form-group"},ue={class:"form-group"},pe={class:"form-buttons"};function me(s,e,d,_,l,n){const o=f("AddTestStepModal");return i(),r("div",{class:"modal-overlay",onClick:e[7]||(e[7]=v(a=>s.$emit("close"),["self"]))},[t("div",ne,[l.localTestCase.id?(i(),r("h3",le,"Edit Test Case")):(i(),r("h3",ae,"Add New Test Case")),t("form",{onSubmit:e[6]||(e[6]=v((...a)=>n.save&&n.save(...a),["prevent"]))},[t("div",ie,[e[8]||(e[8]=t("label",{for:"title"},"Test Case Title",-1)),h(t("input",{type:"text",id:"title","onUpdate:modelValue":e[0]||(e[0]=a=>l.localTestCase.title=a),class:"form-control",required:""},null,512),[[T,l.localTestCase.title]])]),t("div",de,[e[10]||(e[10]=t("label",{for:"functionality"},"Functionality",-1)),h(t("select",{id:"functionality","onUpdate:modelValue":e[1]||(e[1]=a=>l.localTestCase.functionality=a),class:"form-control",required:""},[e[9]||(e[9]=t("option",{value:"",disabled:""},"Select Functionality",-1)),(i(!0),r(y,null,M(d.functionalities,a=>(i(),r("option",{key:a.id,value:a.id},u(a.name),9,re))),128))],512),[[$,l.localTestCase.functionality]])]),t("div",ce,[e[11]||(e[11]=t("label",{for:"description"},"Description",-1)),h(t("textarea",{id:"description","onUpdate:modelValue":e[2]||(e[2]=a=>l.localTestCase.description=a),class:"form-control"},null,512),[[T,l.localTestCase.description]])]),t("div",ue,[e[12]||(e[12]=t("label",{for:"expected_result"},"Expected Result",-1)),h(t("input",{type:"text",id:"expected_result","onUpdate:modelValue":e[3]||(e[3]=a=>l.localTestCase.expected_result=a),class:"form-control",required:""},null,512),[[T,l.localTestCase.expected_result]])]),t("div",pe,[e[13]||(e[13]=t("button",{type:"submit",class:"btn btn-primary"},"Create",-1)),t("button",{type:"button",onClick:e[4]||(e[4]=a=>s.$emit("close")),class:"btn btn-secondary"},"Cancel"),t("button",{type:"button",onClick:e[5]||(e[5]=(...a)=>n.openAddStepModal&&n.openAddStepModal(...a)),class:"btn btn-info"},"Add Step")])],32),l.showAddStepModal?(i(),C(o,{key:2,testCaseId:l.localTestCase.id,onClose:n.closeAddStepModal,onSaved:n.handleStepSaved},null,8,["testCaseId","onClose","onSaved"])):b("",!0)])])}const he=S(oe,[["render",me],["__scopeId","data-v-6cac7727"]]),fe={props:{testCase:Object},data(){return{testers:[],selectedUser:null}},async mounted(){const s=await p.get("/users/?role=tester");this.testers=s.data},methods:{assign(){this.$emit("assign",{testCaseId:this.testCase.id,userId:this.selectedUser})}}},Ce={class:"modal-overlay"},be={class:"modal-content"},Te=["value"],Se={class:"form-buttons"};function _e(s,e,d,_,l,n){return i(),r("div",Ce,[t("div",be,[e[5]||(e[5]=t("h3",null,"Assign Test Case",-1)),t("form",{onSubmit:e[2]||(e[2]=v((...o)=>n.assign&&n.assign(...o),["prevent"]))},[e[4]||(e[4]=t("label",null,"Select User",-1)),h(t("select",{"onUpdate:modelValue":e[0]||(e[0]=o=>l.selectedUser=o),class:"form-control"},[(i(!0),r(y,null,M(l.testers,o=>(i(),r("option",{key:o.id,value:o.id},u(o.first_name)+" - "+u(o.organization_name),9,Te))),128))],512),[[$,l.selectedUser]]),t("div",Se,[e[3]||(e[3]=t("button",{type:"submit",class:"btn btn-primary"},"Assign",-1)),t("button",{type:"button",onClick:e[1]||(e[1]=o=>s.$emit("close")),class:"btn btn-secondary"},"Cancel")])],32)])])}const ve=S(fe,[["render",_e]]),ye={components:{AddTestStepModal:A},props:{testCase:Object},data(){return{showStepModal:!1,stepToEdit:null}},methods:{openAddStepModal(){this.stepToEdit=null,this.showStepModal=!0},openEditStepModal(s){this.stepToEdit={...s},this.showStepModal=!0},closeStepModal(){this.showStepModal=!1},async fetchTestSteps(){var s;if((s=this.testCase)!=null&&s.id)try{const e=await p.get(`/test-cases/${this.testCase.id}/`);this.$emit("update:testCase",e.data)}catch(e){console.error("Error fetching test steps:",e),this.$emit("error",e)}},async deleteStep(s){try{await p.delete(`/test-steps/${s}/`),this.fetchTestSteps()}catch(e){console.error("Error deleting test step:",e),this.$emit("error",e)}},handleError(s){console.error("Error in AddTestStepModal:",s),this.$emit("error",s)}},mounted(){this.fetchTestSteps()}},Me={class:"modal-overlay"},ge={class:"modal-content"},Ae={class:"modal-title"},we={class:"table"},ke=["href"],Ee={key:1},$e=["onClick"],xe=["onClick"];function Ue(s,e,d,_,l,n){var a;const o=f("AddTestStepModal");return i(),r("div",Me,[t("div",ge,[t("h3",Ae,"Test Steps for "+u((a=d.testCase)==null?void 0:a.title),1),t("table",we,[e[1]||(e[1]=t("thead",null,[t("tr",null,[t("th",null,"Step Number"),t("th",null,"Description"),t("th",null,"Expected Result"),t("th",null,"Attachment"),t("th",null,"Actions")])],-1)),t("tbody",null,[(i(!0),r(y,null,M(d.testCase.steps,c=>(i(),r("tr",{key:c.id},[t("td",null,u(c.step_number),1),t("td",null,u(c.description),1),t("td",null,u(c.expected_result),1),t("td",null,[c.attachment?(i(),r("a",{key:0,href:c.attachment,target:"_blank",class:"attachment-link"}," View Attachment ",8,ke)):(i(),r("span",Ee,"No Attachment"))]),t("td",null,[t("button",{onClick:m=>n.openEditStepModal(c),class:"btn btn-warning btn-sm"},"Edit",8,$e),t("button",{onClick:m=>n.deleteStep(c.id),class:"btn btn-danger btn-sm"},"Delete",8,xe)])]))),128))])]),t("button",{onClick:e[0]||(e[0]=c=>s.$emit("close")),class:"btn btn-secondary"},"Close"),l.showStepModal?(i(),C(o,{key:0,testCaseId:d.testCase.id,stepToEdit:l.stepToEdit,onClose:n.closeStepModal,onSaved:n.fetchTestSteps,onError:n.handleError},null,8,["testCaseId","stepToEdit","onClose","onSaved","onError"])):b("",!0)])])}const Ne=S(ye,[["render",Ue],["__scopeId","data-v-72fc733e"]]),g=E(),Ve={components:{TestCaseTable:W,TestCaseModal:he,TestCaseAssignmentModal:ve,TestStepsView:Ne,AddTestStepModal:A},data(){return{testCases:[],functionalities:[],selectedTestCase:null,showModal:!1,showAssignModal:!1,showStepsModal:!1,showAddStepModal:!1}},computed:{testCasesWithFunctionalityNames(){return this.testCases.map(s=>{const e=this.functionalities.find(d=>d.id===s.functionality);return{...s,functionalityName:e?e.name:"N/A"}})}},methods:{async fetchTestCases(){try{const s=await p.get("/test-cases/");this.testCases=s.data}catch(s){console.error("Error fetching test cases:",s)}},async fetchFunctionalities(){try{const s=await p.get("/functionalities/");this.functionalities=s.data}catch(s){console.error("Error fetching functionalities:",s)}},openCreateModal(){this.selectedTestCase=null,this.showModal=!0},editTestCase(s){this.selectedTestCase={...s},this.showModal=!0},openAssignModal(s){this.selectedTestCase={...s},this.showAssignModal=!0},openTestSteps(s){this.selectedTestCase={...s},this.showStepsModal=!0},openAddStepModal(s){this.selectedTestCase={...s},this.showAddStepModal=!0},closeModal(){this.showModal=!1,this.fetchTestCases()},closeAssignModal(){this.showAssignModal=!1,this.fetchTestCases()},closeTestSteps(){this.showStepsModal=!1},closeAddStepModal(){this.showAddStepModal=!1},async assignUser({testCaseId:s,userId:e}){try{await p.post(`/test-cases/${s}/assign/`,{userId:e}),this.closeAssignModal(),this.fetchTestCases(),g.success("User assigned successfully!")}catch(d){console.error("Error assigning user:",d),d.response?g.error("Error assigning user: "+d.response.data.error):g.error("An unexpected error occurred.")}},async deleteTestCase(s){confirm("Are you sure you want to delete this test case?")&&(await p.delete(`/test-cases/${s}/`),this.fetchTestCases())},async saveTestCase(s){s.id?await p.put(`/test-cases/${s.id}/`,s):await p.post("/test-cases/",s),this.closeModal()},handleStepSaved(){this.fetchTestCases()}},mounted(){this.fetchTestCases(),this.fetchFunctionalities()}},Ie={class:"container mt-4"};function Fe(s,e,d,_,l,n){var w,k;const o=f("TestCaseTable"),a=f("TestCaseModal"),c=f("TestCaseAssignmentModal"),m=f("TestStepsView"),x=f("AddTestStepModal");return i(),r("div",Ie,[e[0]||(e[0]=t("h2",{class:"mb-4"},"Test Case Management",-1)),N(o,{testCases:n.testCasesWithFunctionalityNames,onOpenModal:n.openCreateModal,onEdit:n.editTestCase,onDelete:n.deleteTestCase,onAssign:n.openAssignModal,onViewSteps:n.openTestSteps,onAddStep:n.openAddStepModal},null,8,["testCases","onOpenModal","onEdit","onDelete","onAssign","onViewSteps","onAddStep"]),l.showModal?(i(),C(a,{key:0,testCase:l.selectedTestCase,functionalities:l.functionalities,onClose:n.closeModal,onSave:n.saveTestCase},null,8,["testCase","functionalities","onClose","onSave"])):b("",!0),l.showAssignModal?(i(),C(c,{key:1,testCase:l.selectedTestCase,onClose:n.closeAssignModal,onAssign:n.assignUser},null,8,["testCase","onClose","onAssign"])):b("",!0),l.showStepsModal?(i(),C(m,{key:2,testCase:l.selectedTestCase,onClose:n.closeTestSteps},null,8,["testCase","onClose"])):b("",!0),l.showAddStepModal?(i(),C(x,{key:3,testCaseId:(w=l.selectedTestCase)==null?void 0:w.id,testCaseTitle:(k=l.selectedTestCase)==null?void 0:k.title,onClose:n.closeAddStepModal,onSaved:n.handleStepSaved},null,8,["testCaseId","testCaseTitle","onClose","onSaved"])):b("",!0)])}const qe=S(Ve,[["render",Fe]]);export{qe as default};
