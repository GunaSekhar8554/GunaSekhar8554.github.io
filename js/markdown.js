// Assuming a 'markdown-it' global
const md = window.markdownit({
  html: true,
  xhtmlOut: true,
  breaks: false,
  linkify: false,
  typographer: false,
  // highlight: function (/*str, lang*/) { return ''; }
})
var mdArray = document.getElementsByTagName("markdown");
for (i = 0; i < Object.keys(mdArray).length; i++) {
  mdArray[i].innerHTML = mdArray[i].textContent
    .replace(/@tweet\[.*\]\(.*\)/g, 
                match => "<blockquote class=twitter-tweet><a href="
                + match.replace(/@tweet\[.*\]\(/, "").replace(/\)/, "")
                + ">"
                + match.replace(/@tweet\[/,"").replace(/\]\(.*\)/)
                + "</a></blockquote>"
               ) 
  mdArray[i].innerHTML = md.render(mdArray[i].innerHTML)
}