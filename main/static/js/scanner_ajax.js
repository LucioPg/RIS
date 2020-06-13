// da copiare direttamente nell html a causa di {% static 'barcode.csv' %}


var init;
    const logFileText = async file => {
        const response = await fetch(file);
        const text = await response.text();
        all = text.split('\n');
        if (init !== all.length) {
            console.log(all.length, init);
            init = all.length;
            console.log('changed');
            var arr=[];
            all.forEach(el => {
                el=el.split(',');
                arr.push(el);
            });
             console.log(arr);

            createTable(arr);

        }

    };

    function createTable(array) {
        var content = "";
        array.forEach(function (row) {
            content += "<tr>";
            row.forEach(function (cell) {
                content += "<td>" + cell + "</td>";
            });
            content += "</tr>";
        });
        document.getElementById("t1").innerHTML = content;
    };

    let file = "barcode.csv";
    // let file = "{{ csv }}";
    logFileText(file);
    setInterval(async () => {
        await logFileText(file);
    }, 500);