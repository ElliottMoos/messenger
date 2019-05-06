var tabs = document.querySelector(".tabs")
var panels = document.querySelectorAll(".panel")

tabs.addEventListener('click', function(e){
    if(e.target.tagName == "A"){
        var targetPanel = document.querySelector(e.target.dataset.target);
        panels.forEach(function(panel){
            if(panel == targetPanel){
                panel.classList.add('active');
            } else {
                panel.classList.remove('active')
            }
        })
    }
})