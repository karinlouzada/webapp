let data = {{ words | tojson }};

let list = document.getElementById("myList");

data.forEach((item) => {
    let li = document.createElement("li");
    li.innerText = item;
    list.appendChild(li);
});

