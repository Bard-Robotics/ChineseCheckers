const TX = Math.sin(Math.PI / 3)
const TY = Math.cos(Math.PI / 3)

const PIECE_COLORS = [
    0,
    "#ae3c60",
    "#df473c",
    "#f3c33c",
    "#255e79",
    "#267778",
    "#82b4bb"
]
function attachListeners() {

    function drawBoard(board) {
        const el = document.getElementById("canvas")
        const ctx = el.getContext('2d')
        const BOARD_H = board.length
        const BOARD_W = board[0].length

        const spacing = 600 / (BOARD_H + 2)
        const radius = spacing * 0.18

        ctx.clearRect(0, 0, 600, 600)

        board.forEach((row, y) => {
            row.forEach((el, x) => {
                if (el == -1)
                    return

                let tx = x - y/2 + BOARD_H/4
                let ty = y

                let px = spacing * (tx + 1)
                let py = spacing * (ty + 1)

                ctx.beginPath()
                //ctx.moveTo(px, py + radius)
                ctx.arc(px, py + radius, radius*2, 0, 2*Math.PI)

                if (el == 0)
                    ctx.stroke()
                else {
                    ctx.fillStyle = PIECE_COLORS[el]
                    ctx.fill()
                }
            })
        })
        
    }

    const POLL_INTERVAL = 10000
    async function poll() {
        let url = `/api/game/${GAME_ID}`

        let response = await fetch(url)
        let json = await response.json()
        requestAnimationFrame(time => {
            drawBoard(json.board)
            setTimeout(poll, POLL_INTERVAL)
        })
    }
    poll()

}

if (document.readyState === 'complete' || document.readyState === 'loaded')
    attachListeners()
else 
    document.addEventListener("DOMContentLoaded", attachListeners)
