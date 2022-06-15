let canvas = document.createElement("canvas")
document.body.appendChild(canvas)
canvas.width = window.innerWidth - 300
canvas.height = window.innerHeight - 20
let ctx = canvas.getContext("2d")
const max_ratio = 100
const min_ratio = 20
ctx.strokeRect(0, 0, canvas.width, canvas.height)
setInterval(() => {
    fetch("/api/image/random")
        .then(d => {
            if (d.status != 200) { throw d }
            return d.blob()
        })
        .then(blob => {
            createImageBitmap(blob).then(img => {
                let ratio = (Math.random() * (max_ratio - min_ratio + 1) + min_ratio) / 100
                let dx = ratio * img.width
                let dy = ratio * img.height
                let x = Math.random() * canvas.width
                let y = Math.random() * canvas.height
                let degrees = Math.random() * 360
                ctx.save()
                ctx.translate(x, y)
                ctx.rotate(degrees * Math.PI / 180)
                ctx.drawImage(img, 0, 0, dx, dy)
                ctx.restore()
            })
        })
}, 1000)