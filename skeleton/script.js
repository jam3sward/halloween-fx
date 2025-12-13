const asyncPost = async (url, content) => {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: content
        });
    } catch(error) {
    } 
}