        if (data.message === 'Message sent successfully!') {
            // alert('Your message has been sent successfully!');
            feedbackElement.textContent = 'तुमचा संदेश यशस्वीपणे पाठवला गेला!';
            feedbackElement.style.color = 'green';
            document.getElementById('contactForm').reset();
        } else {
            // alert('Failed to send your message.');
            feedbackElement.textContent = 'तुमचा संदेश पाठवण्यात अयशस्वी!';
            feedbackElement.style.color = 'red';
        }