function attachListeners() {

    document.getElementById("join-game").addEventListener("submit", e => {
        let id = document.getElementById("join-id").value.toUpperCase()
        let room_url = `/room/${id}`
        // Check if it exists
        fetch(room_url, {method: "HEAD"})            
            .then(resp => {
                if (resp.ok)
                    window.location.href = room_url
                else
                    alert("That room doesn't exist.")

            })
        
    })

}

if (document.readyState === 'complete' || document.readyState === 'loaded')
    attachListeners()
else 
    document.addEventListener("DOMContentLoaded", attachListeners)
