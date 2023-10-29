!function(){"use strict";var t=tinymce.util.Tools.resolve("tinymce.PluginManager");const e=(null,t=>null===t);const n=t=>t,o=(t,e)=>{const n=t.length,o=new Array(n);for(let r=0;r<n;r++){const n=t[r];o[r]=e(n,r)}return o},r="[-'\\.‘’․﹒＇．]",c="[:··״‧︓﹕：]",u="[±+*/,;;։،؍٬߸⁄︐︔﹐﹔，；]",s="[0-9٠-٩٫۰-۹߀-߉०-९০-৯੦-੯૦-૯୦-୯௦-௯౦-౯೦-೯൦-൯๐-๙໐-໙༠-༩၀-၉႐-႙០-៩᠐-᠙᥆-᥏᧐-᧙᪀-᪉᪐-᪙᭐-᭙᮰-᮹᱀-᱉᱐-᱙꘠-꘩꣐-꣙꤀-꤉꧐-꧙꩐-꩙꯰-꯹]",a="\\r",l="\\n",i="[\v\f\u2028\u2029]",d="[̀-ͯ҃-҉֑-ׇֽֿׁׂׅׄؐ-ًؚ-ٰٟۖ-ۜ۟-۪ۤۧۨ-ܑۭܰ-݊ަ-ް߫-߳ࠖ-࠙ࠛ-ࠣࠥ-ࠧࠩ-࡙࠭-࡛ऀ-ःऺ-़ा-ॏ॑-ॗॢॣঁ-ঃ়া-ৄেৈো-্ৗৢৣਁ-ਃ਼ਾ-ੂੇੈੋ-੍ੑੰੱੵઁ-ઃ઼ા-ૅે-ૉો-્ૢૣଁ-ଃ଼ା-ୄେୈୋ-୍ୖୗୢୣஂா-ூெ-ைொ-்ௗఁ-ఃా-ౄె-ైొ-్ౕౖౢౣಂಃ಼ಾ-ೄೆ-ೈೊ-್ೕೖೢೣംഃാ-ൄെ-ൈൊ-്ൗൢൣංඃ්ා-ුූෘ-ෟෲෳัิ-ฺ็-๎ັິ-ູົຼ່-ໍ༹༘༙༵༷༾༿ཱ-྄྆྇ྍ-ྗྙ-ྼ࿆ါ-ှၖ-ၙၞ-ၠၢ-ၤၧ-ၭၱ-ၴႂ-ႍႏႚ-ႝ፝-፟ᜒ-᜔ᜲ-᜴ᝒᝓᝲᝳា-៓៝᠋-᠍ᢩᤠ-ᤫᤰ-᤻ᦰ-ᧀᧈᧉᨗ-ᨛᩕ-ᩞ᩠-᩿᩼ᬀ-ᬄ᬴-᭄᭫-᭳ᮀ-ᮂᮡ-᯦᮪-᯳ᰤ-᰷᳐-᳔᳒-᳨᳭ᳲ᷀-ᷦ᷼-᷿‌‍⃐-⃰⳯-⵿⳱ⷠ-〪ⷿ-゙゚〯꙯-꙲꙼꙽꛰꛱ꠂ꠆ꠋꠣ-ꠧꢀꢁꢴ-꣄꣠-꣱ꤦ-꤭ꥇ-꥓ꦀ-ꦃ꦳-꧀ꨩ-ꨶꩃꩌꩍꩻꪰꪲ-ꪴꪷꪸꪾ꪿꫁ꯣ-ꯪ꯬꯭ﬞ︀-️︠-︦ﾞﾟ]",g="[­؀-؃۝܏឴឵‎‏‪-‮⁠-⁤⁪-⁯\ufeff￹-￻]",p="[〱-〵゛゜゠-ヺー-ヿㇰ-ㇿ㋐-㋾㌀-㍗ｦ-ﾝ]",h="[=_‿⁀⁔︳︴﹍-﹏＿∀-⋿<>]",C="[~№|!-*+-\\/:;?@\\[-`{}¡«·»¿;·՚-՟։֊־׀׃׆׳״؉؊،؍؛؞؟٪-٭۔܀-܍߷-߹࠰-࠾࡞।॥॰෴๏๚๛༄-༒༺-༽྅࿐-࿔࿙࿚၊-၏჻፡-፨᐀᙭᙮᚛᚜᛫-᛭᜵᜶។-៖៘-៚᠀-᠊᥄᥅᨞᨟᪠-᪦᪨-᪭᭚-᭠᯼-᯿᰻-᰿᱾᱿᳓‐-‧‰-⁃⁅-⁑⁓-⁞⁽⁾₍₎〈〉❨-❵⟅⟆⟦-⟯⦃-⦘⧘-⧛⧼⧽⳹-⳼⳾⳿⵰⸀-⸮⸰⸱、-〃〈-】〔-〟〰〽゠・꓾꓿꘍-꘏꙳꙾꛲-꛷꡴-꡷꣎꣏꣸-꣺꤮꤯꥟꧁-꧍꧞꧟꩜-꩟꫞꫟꯫﴾﴿︐-︙︰-﹒﹔-﹡﹣﹨﹪﹫！-＃％-＊，-／：；？＠［-］＿｛｝｟-･]",y=10,m=[new RegExp("[A-Za-zªµºÀ-ÖØ-öø-ˁˆ-ˑˠ-ˤˬˮͰ-ʹͶͷͺ-ͽΆΈ-ΊΌΎ-ΡΣ-ϵϷ-ҁҊ-ԧԱ-Ֆՙա-ևא-תװ-׳ؠ-يٮٯٱ-ۓەۥۦۮۯۺ-ۼۿܐܒ-ܯݍ-ޥޱߊ-ߪߴߵߺࠀ-ࠕࠚࠤࠨࡀ-ࡘऄ-हऽॐक़-ॡॱ-ॷॹ-ॿঅ-ঌএঐও-নপ-রলশ-হঽৎড়ঢ়য়-ৡৰৱਅ-ਊਏਐਓ-ਨਪ-ਰਲਲ਼ਵਸ਼ਸਹਖ਼-ੜਫ਼ੲ-ੴઅ-ઍએ-ઑઓ-નપ-રલળવ-હઽૐૠૡଅ-ଌଏଐଓ-ନପ-ରଲଳଵ-ହଽଡ଼ଢ଼ୟ-ୡୱஃஅ-ஊஎ-ஐஒ-கஙசஜஞடணதந-பம-ஹௐఅ-ఌఎ-ఐఒ-నప-ళవ-హఽౘౙౠౡಅ-ಌಎ-ಐಒ-ನಪ-ಳವ-ಹಽೞೠೡೱೲഅ-ഌഎ-ഐഒ-ഺഽൎൠൡൺ-ൿඅ-ඖක-නඳ-රලව-ෆༀཀ-ཇཉ-ཬྈ-ྌႠ-Ⴥა-ჺჼᄀ-ቈቊ-ቍቐ-ቖቘቚ-ቝበ-ኈኊ-ኍነ-ኰኲ-ኵኸ-ኾዀዂ-ዅወ-ዖዘ-ጐጒ-ጕጘ-ፚᎀ-ᎏᎠ-Ᏼᐁ-ᙬᙯ-ᙿᚁ-ᚚᚠ-ᛪᛮ-ᛰᜀ-ᜌᜎ-ᜑᜠ-ᜱᝀ-ᝑᝠ-ᝬᝮ-ᝰᠠ-ᡷᢀ-ᢨᢪᢰ-ᣵᤀ-ᤜᨀ-ᨖᬅ-ᬳᭅ-ᭋᮃ-ᮠᮮᮯᯀ-ᯥᰀ-ᰣᱍ-ᱏᱚ-ᱽᳩ-ᳬᳮ-ᳱᴀ-ᶿḀ-ἕἘ-Ἕἠ-ὅὈ-Ὅὐ-ὗὙὛὝὟ-ώᾀ-ᾴᾶ-ᾼιῂ-ῄῆ-ῌῐ-ΐῖ-Ίῠ-Ῥῲ-ῴῶ-ῼⁱⁿₐ-ₜℂℇℊ-ℓℕℙ-ℝℤΩℨK-ℭℯ-ℹℼ-ℿⅅ-ⅉⅎⅠ-ↈⒶ-ⓩⰀ-Ⱞⰰ-ⱞⱠ-ⳤⳫ-ⳮⴀ-ⴥⴰ-ⵥⵯⶀ-ⶖⶠ-ⶦⶨ-ⶮⶰ-ⶶⶸ-ⶾⷀ-ⷆⷈ-ⷎⷐ-ⷖⷘ-ⷞⸯ々〻〼ㄅ-ㄭㄱ-ㆎㆠ-ㆺꀀ-ꒌꓐ-ꓽꔀ-ꘌꘐ-ꘟꘪꘫꙀ-ꙮꙿ-ꚗꚠ-ꛯꜗ-ꜟꜢ-ꞈꞋ-ꞎꞐꞑꞠ-ꞩꟺ-ꠁꠃ-ꠅꠇ-ꠊꠌ-ꠢꡀ-ꡳꢂ-ꢳꣲ-ꣷꣻꤊ-ꤥꤰ-ꥆꥠ-ꥼꦄ-ꦲꧏꨀ-ꨨꩀ-ꩂꩄ-ꩋꬁ-ꬆꬉ-ꬎꬑ-ꬖꬠ-ꬦꬨ-ꬮꯀ-ꯢ가-힣ힰ-ퟆퟋ-ퟻﬀ-ﬆﬓ-ﬗיִײַ-ﬨשׁ-זּטּ-לּמּנּסּףּפּצּ-ﮱﯓ-ﴽﵐ-ﶏﶒ-ﷇﷰ-ﷻﹰ-ﹴﹶ-ﻼＡ-Ｚａ-ｚﾠ-ﾾￂ-ￇￊ-ￏￒ-ￗￚ-ￜ]"),new RegExp(r),new RegExp(c),new RegExp(u),new RegExp(s),new RegExp(a),new RegExp(l),new RegExp(i),new RegExp(d),new RegExp(g),new RegExp(p),new RegExp(h),new RegExp("@")],w=new RegExp("^"+C+"$"),W=m,f=t=>{let e=13;const n=W.length;for(let o=0;o<n;++o){const n=W[o];if(n&&n.test(t)){e=o;break}}return e},x=(t,e)=>{const n=t[e],o=t[e+1];if(e<0||e>t.length-1&&0!==e)return!1;if(0===n&&0===o)return!1;const r=t[e+2];if(0===n&&(2===o||1===o||12===o)&&0===r)return!1;const c=t[e-1];return(2!==n&&1!==n&&12!==o||0!==o||0!==c)&&(4!==n&&0!==n||4!==o&&0!==o)&&(3!==n&&1!==n||4!==o||4!==c)&&(4!==n||3!==o&&1!==o||4!==r)&&(8!==n&&9!==n||0!==o&&4!==o&&o!==y&&8!==o&&9!==o)&&(8!==o&&(9!==o||0!==r&&4!==r&&r!==y&&8!==r&&9!==r)||0!==n&&4!==n&&n!==y&&8!==n&&9!==n)&&(5!==n||6!==o)&&(7===n||5===n||6===n||7===o||5===o||6===o||(n!==y||o!==y)&&(11!==o||0!==n&&4!==n&&n!==y&&11!==n)&&(11!==n||0!==o&&4!==o&&o!==y)&&12!==n)},E=/^\s+$/,R=w,S=t=>"http"===t||"https"===t,b=(t,e)=>{const n=((t,e)=>{let n;for(n=e;n<t.length&&!E.test(t[n]);n++);return n})(t,e+1);return"://"===t.slice(e+1,n).join("").substr(0,3)?n:e},v=(t,e,n)=>((t,e,n)=>{n={includeWhitespace:!1,includePunctuation:!1,...n};const r=o(t,e);return((t,e,n,o)=>{const r=[],c=[];let u=[];for(let s=0;s<n.length;++s)if(u.push(t[s]),x(n,s)){const n=e[s];if((o.includeWhitespace||!E.test(n))&&(o.includePunctuation||!R.test(n))){const n=s-u.length+1,o=s+1,a=e.slice(n,o).join("");if(S(a)){const n=b(e,s),r=t.slice(o,n);Array.prototype.push.apply(u,r),s=n}r.push(u),c.push({start:n,end:o})}u=[]}return{words:r,indices:c}})(t,r,(t=>{const e=(t=>{const e={};return n=>{if(e[n])return e[n];{const o=t(n);return e[n]=o,o}}})(f);return o(t,e)})(r),n)})(t,e,n).words;var F=tinymce.util.Tools.resolve("tinymce.dom.TreeWalker");const T=(t,e)=>{const n=e.getBlockElements(),o=e.getVoidElements(),r=t=>n[t.nodeName]||o[t.nodeName],c=[];let u="";const s=new F(t,t);let a;for(;a=s.next();)3===a.nodeType?u+=a.data.replace(/\uFEFF/g,""):r(a)&&u.length&&(c.push(u),u="");return u.length&&c.push(u),c},A=t=>t.replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g,"_").length,B=(t,e)=>{const o=(t=>t.replace(/\u200B/g,""))(T(t,e).join("\n"));return v(o.split(""),n).length},D=(t,e)=>{const n=T(t,e).join("");return A(n)},j=(t,e)=>{const n=T(t,e).join("").replace(/\s/g,"");return A(n)},k=(t,e)=>()=>e(t.getBody(),t.schema),U=(t,e)=>()=>e(t.selection.getRng().cloneContents(),t.schema),M=t=>k(t,B);var P=tinymce.util.Tools.resolve("tinymce.util.Delay");const N=(t,e)=>{((t,e)=>{t.dispatch("wordCountUpdate",{wordCount:{words:e.body.getWordCount(),characters:e.body.getCharacterCount(),charactersWithoutSpaces:e.body.getCharacterCountWithoutSpaces()}})})(t,e)},V=(t,n,o)=>{const r=((t,n)=>{let o=null;return{cancel:()=>{e(o)||(clearTimeout(o),o=null)},throttle:(...r)=>{e(o)&&(o=setTimeout((()=>{o=null,t.apply(null,r)}),n))}}})((()=>N(t,n)),o);t.on("init",(()=>{N(t,n),P.setEditorTimeout(t,(()=>{t.on("SetContent BeforeAddUndo Undo Redo ViewUpdate keyup",r.throttle)}),0),t.on("remove",r.cancel)}))};((e=300)=>{t.add("wordcount",(t=>{const n=(t=>({body:{getWordCount:M(t),getCharacterCount:k(t,D),getCharacterCountWithoutSpaces:k(t,j)},selection:{getWordCount:U(t,B),getCharacterCount:U(t,D),getCharacterCountWithoutSpaces:U(t,j)},getCount:M(t)}))(t);return((t,e)=>{t.addCommand("mceWordCount",(()=>((t,e)=>{t.windowManager.open({title:"Word Count",body:{type:"panel",items:[{type:"table",header:["Count","Document","Selection"],cells:[["Words",String(e.body.getWordCount()),String(e.selection.getWordCount())],["Characters (no spaces)",String(e.body.getCharacterCountWithoutSpaces()),String(e.selection.getCharacterCountWithoutSpaces())],["Characters",String(e.body.getCharacterCount()),String(e.selection.getCharacterCount())]]}]},buttons:[{type:"cancel",name:"close",text:"Close",primary:!0}]})})(t,e)))})(t,n),(t=>{const e=()=>t.execCommand("mceWordCount");t.ui.registry.addButton("wordcount",{tooltip:"Word count",icon:"character-count",onAction:e}),t.ui.registry.addMenuItem("wordcount",{text:"Word count",icon:"character-count",onAction:e})})(t),V(t,n,e),n}))})()}();