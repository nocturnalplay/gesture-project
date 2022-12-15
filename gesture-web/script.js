// function move(e) {
//     console.log(e.clientX)
//     const mouse = document.getElementById("mouse");
//     mouse.style.left = e.clientX + "px"
//     mouse.style.top = e.clientY + "px"
// }
window.onload = () => {
    const ws = new WebSocket("ws://127.0.0.1:3333")

    ws.onopen = () => {
        console.log("web socket connected")
    }
    ws.onmessage = (e) => {
        console.log(JSON.parse(e.data))
        let { tx, ty, sx, sy, rx, ry } = JSON.parse(e.data)
       
        const t = document.getElementById("t");
        const s = document.getElementById("s");
        const r = document.getElementById("r");

        t.style.left = 100 - Math.abs(tx) + "%"
        t.style.top =  Math.abs(ty) + "%"
        t.style.boxShadow = `0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)})`
        
        s.style.left = 100 - Math.abs(sx) + "%"
        s.style.top =  Math.abs(sy) + "%"
        s.style.boxShadow = `0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)})`
        
        r.style.left = 100 - Math.abs(rx) + "%"
        r.style.top =  Math.abs(ry) + "%"
        r.style.boxShadow = `0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)}),
        0 0 40px rgb(${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)},${Math.floor(Math.random() * 256)})`
    
    }
}