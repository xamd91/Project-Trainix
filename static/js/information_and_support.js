function downloadGuide(url, filename) {
    fetch(url)
        .then(response => { 
            if (!response.ok) throw new Error('File not found' + url);
            return response.blob();
        })
        .then(blob => {
            const blobUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(blobUrl);
        })
        .catch(err => {
            console.error('Download failed:', err);
            alert('Sorry, this guide could not be downloaded. Please try again.')
        });
    }