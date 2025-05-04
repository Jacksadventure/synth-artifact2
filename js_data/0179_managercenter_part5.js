document.getElementById('articleList').addEventListener('click', function(event) {
	if (event.target.classList.contains('delete-button')) {
		event.target.parentElement.parentElement.remove();
	} else if (event.target.classList.contains('edit-button')) {
		const articleItem = event.target.parentElement.parentElement;
		const title = articleItem.querySelector('.article-title').innerText;
		document.getElementById('articleTitle').value = title;
		document.getElementById('addArticles').style.display = 'block';
	}
});