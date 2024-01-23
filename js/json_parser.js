// Fetch the file asynchronously
fetch('readings.json')
    .then(response => response.json())
    .then(json => {
    // Create a new object to store the formatted data
    let formatted = {};

    // Loop over the keys of the JSON object, which are the sensor names
    for (let sensor in json) {
      // Create a new object with the same key in the new object
      formatted[sensor] = {};

      // Loop over the keys of the nested object, which are the timestamps
      for (let timestamp in json[sensor]) {
        // Create a Date object from the timestamp
        let date = new Date(timestamp * 1000);

        // Use the toLocaleString method to get the human readable date string
        let dateString = date.toLocaleString();

        // Store the date string and the reading object in the new object under the same sensor name
        formatted[sensor][dateString] = json[sensor][timestamp];
      }
    }

    // Print the formatted object
    data = formatted;

    const times = [];
    const temperatures = [];
    const humidities = [];
    
    for (const [key, value] of Object.entries(data)) {
        for (const [subKey, subValue] of Object.entries(value)) {
            times.push(subKey);
            temperatures.push(subValue.temperature);
            humidities.push(subValue.humidity);
        }
    }



    // table stuff
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");
    
    const headerRow = document.createElement("tr");
    const dateHeader = document.createElement("th");
    dateHeader.textContent = "Date";
    headerRow.appendChild(dateHeader);
    
    const tempMinHeader = document.createElement("th");
    tempMinHeader.textContent = "Temperature Min";
    headerRow.appendChild(tempMinHeader);
    
    const tempMaxHeader = document.createElement("th");
    tempMaxHeader.textContent = "Temperature Max";
    headerRow.appendChild(tempMaxHeader);
    
    const tempMedianHeader = document.createElement("th");
    tempMedianHeader.textContent = "Temperature Median";
    headerRow.appendChild(tempMedianHeader);
    
    const tempMeanHeader = document.createElement("th");
    tempMeanHeader.textContent = "Temperature Mean";
    headerRow.appendChild(tempMeanHeader);
    
    const humidityMinHeader = document.createElement("th");
    humidityMinHeader.textContent = "Humidity Min";
    headerRow.appendChild(humidityMinHeader);
    
    const humidityMaxHeader = document.createElement("th");
    humidityMaxHeader.textContent = "Humidity Max";
    headerRow.appendChild(humidityMaxHeader);
    
    const humidityMedianHeader = document.createElement("th");
    humidityMedianHeader.textContent = "Humidity Median";
    headerRow.appendChild(humidityMedianHeader);
    
    const humidityMeanHeader = document.createElement("th");
    humidityMeanHeader.textContent = "Humidity Mean";
    headerRow.appendChild(humidityMeanHeader);
    
    thead.appendChild(headerRow);
    table.appendChild(thead);
    
    const groupedData = {};
    for (const [key, value] of Object.entries(data)) {
        for (const [subKey, subValue] of Object.entries(value)) {
            const date = subKey.split(",")[0];
            if (!groupedData[date]) {
                groupedData[date] = [];
            }
            groupedData[date].push(subValue);
        }
    }
    
    for (const [date, values] of Object.entries(groupedData)) {
        const temperatures = values.map(v => v.temperature);
        const humidities = values.map(v => v.humidity);
    
        const row = document.createElement("tr");
    
        const dateCell = document.createElement("td");
        dateCell.textContent = date;
        row.appendChild(dateCell);
    
        const tempMinCell = document.createElement("td");
        tempMinCell.textContent = Math.min(...temperatures);
        row.appendChild(tempMinCell);
    
        const tempMaxCell = document.createElement("td");
        tempMaxCell.textContent = Math.max(...temperatures);
        row.appendChild(tempMaxCell);
    
        const tempMedianCell = document.createElement("td");
        tempMedianCell.textContent = getMedian(temperatures);
        row.appendChild(tempMedianCell);
    
        const tempMeanCell = document.createElement("td");
        tempMeanCell.textContent = getMean(temperatures);
        row.appendChild(tempMeanCell);
    
        const humidityMinCell = document.createElement("td");
        humidityMinCell.textContent = Math.min(...humidities);
        row.appendChild(humidityMinCell);
    
        const humidityMaxCell = document.createElement("td");
        humidityMaxCell.textContent = Math.max(...humidities);
        row.appendChild(humidityMaxCell);
    
        const humidityMedianCell = document.createElement("td");
        humidityMedianCell.textContent = getMedian(humidities);
        row.appendChild(humidityMedianCell);
    
        const humidityMeanCell = document.createElement("td");
        humidityMeanCell.textContent = getMean(humidities);
        row.appendChild(humidityMeanCell);
    
        tbody.appendChild(row);
    }
    
    table.appendChild(tbody);
    
    const container = document.querySelector("#stats-table-container");
    container.innerHTML = "";
    container.appendChild(table);
        
    function getMedian(arr) {
        const sorted = arr.slice().sort((a, b) => a - b);
        const middle = Math.floor(sorted.length / 2);
    
        if (sorted.length % 2 === 0) {
            return (sorted[middle - 1] + sorted[middle]) / 2;
        }
    
        return sorted[middle];
    }
    
    function getMean(arr) {
        return arr.reduce((a, b) => a + b, 0) / arr.length;
    }
    // end table stuff


    //graph stuff
    const temperatureTrace = {
        x: times,
        y: temperatures,
        mode: "lines",
        name: "Temperature"
    };
    
    const humidityTrace = {
        x: times,
        y: humidities,
        mode: "lines",
        name: "Humidity"
    };
    
    const layout = {
        title: "Temperature and Humidity vs. Time",
        xaxis: {
            title: "Time"
        },
        yaxis: {
            title: "Temperature/Humidity"
        }
    };
    
    const graph_data = [temperatureTrace, humidityTrace];
    
    Plotly.newPlot("graph", graph_data, layout);
    //end graph stuff
});