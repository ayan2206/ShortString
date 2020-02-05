
class Item {
    constructor(label, url) {
      this.label = label
      this.url = url
    }
  }

function buttonClick() {
    var select = document.getElementById("chooseOption")
    var val = select.options[select.selectedIndex].value
    console.log(val)

    var dataSource = []

    var urlStr = 'http://127.0.0.1:5000/todo/api/v1.0/tasks/'
    var request = new XMLHttpRequest()
    request.open('GET', urlStr, true)
    request.onload = function() {
        
        var data = JSON.parse(this.response)

        var mainBody = document.getElementById("mainBody")
        var table = document.createElement("TABLE")
        table.setAttribute("id", "myTable");
        mainBody.appendChild(table)
        

        data.forEach(element => {
            console.log(element.itemLabel)
            console.log(element.itemUrl)

            var item = new Item(element.itemLabel, element.itemUrl)
            dataSource.push(item)

            var row = document.createElement("TR")
            // row.setAttribute("id", "myTr")
            table.appendChild(row)
            // document.getElementById("myTable").appendChild(y)

            var column1 = document.createElement("TD")
            var label = document.createTextNode(item.label)
            column1.appendChild(label)
            row.appendChild(column1)

            var column2 = document.createElement("TD")
            var url = document.createTextNode(item.url)
            column2.appendChild(url)
            row.appendChild(column2)

            var column3 = document.createElement("TD")
            var btn = document.createElement("BUTTON")
            btn.innerHTML = "Find Short String"
            column3.appendChild(btn)
            row.appendChild(column3)
        });

    }
    request.send()
}


var request = new XMLHttpRequest()
request.open('GET', 'https://ghibliapi.herokuapp.com/films', true)
request.onload = function() {
    // accessing JSON here
    var data = JSON.parse(this.response)
    
    if (request.status >= 200 && request.status < 400) {
        
    } else {
        console.log('error')

        const errorMessage = document.createElement('marquee')
        errorMessage.textContent = `Gah, it's not working!`
        app.appendChild(errorMessage)
    }
}
request.send()

