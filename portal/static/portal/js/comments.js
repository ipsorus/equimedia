const commentForm = document.forms.commentForm;
const commentFormContent = commentForm.content;
const commentFormParentInput = commentForm.parent;
const commentFormSubmit = commentForm.commentSubmit;
const commentPostId = commentForm.getAttribute('data-post-id');
const commentTarget = commentForm.getAttribute('data-post-name-format');

commentForm.addEventListener('submit', createComment);

replyUser()

function replyUser() {
  document.querySelectorAll('.btn-reply').forEach(e => {
    e.addEventListener('click', replyComment);
  });
}

function replyComment() {
  const commentUsername = this.getAttribute('data-comment-username');
  const commentMessageId = this.getAttribute('data-comment-id');
  commentFormContent.value = ``;
  commentFormParentInput.value = commentMessageId;
}
async function createComment(event) {
    event.preventDefault();
    commentFormSubmit.disabled = true;
    commentFormSubmit.innerText = "Ожидаем ответа сервера";
    try {
        const response = await fetch(`/${commentTarget}/${commentPostId}/comments/create/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: new FormData(commentForm),
        });
        const comment = await response.json();

        let commentTemplate = `<li class="comment even thread-even" id="li-comment-${comment.id}">
                                    <div id="comment-${comment.id}" class="comment-wrap">
                                        <div class="comment-meta">
                                            <div class="comment-author vcard">
                                                <span class="comment-avatar">
                                                <img alt='Image' src='${comment.avatar}' class='avatar avatar-60 photo avatar-default' height='60' width='60'></span>
                                            </div>
                                        </div>
                                        <div class="comment-content">
                                            <div class="comment-author"><a href="${comment.get_absolute_url}" title="Ссылка на профиль автора комментария">${comment.author}</a><a href="#comment-${comment.id}" title="Ссылка на комментарий"> #</a><span>Добавлен только что</span></div>
                                            <p>${comment.content}</p>
                                            <a class='comment-reply-link btn-reply' href="#commentForm" data-comment-id="${comment.id}" data-comment-username="${comment.author}" title="Ответить на комментарий"><i class="bi-reply-fill"></i></a>
                                        </div>
                                        <div class="clear"></div>
                                    </div>
                                </li>`;

        let commentChildTemplate = `<li class="comment even thread-even" id="li-comment-${comment.id}">
                                    <div id="comment-${comment.id}" class="comment-wrap">
                                        <div class="comment-meta">
                                            <div class="comment-author vcard">
                                                <span class="comment-avatar">
                                                <img alt='Image' src='${comment.avatar}' class='avatar avatar-60 photo avatar-default' height='60' width='60'></span>
                                            </div>
                                        </div>
                                        <div class="comment-content">
                                            <div class="comment-author"><a href="${comment.get_absolute_url}" title="Ссылка на профиль автора комментария">${comment.author}</a><a href="#comment-${comment.id}" title="Ссылка на комментарий"> #</a> <i class="bi-arrow-right"></i> <a href="#comm-${comment.parent_id}" title="Ссылка на комментарий-источник">${comment.parent_author}</a><span>Добавлен только что</span></div>
                                                <div class="quote-bubble quote-bubble-left mb-3 mt-4">
                                                    <span>${comment.parent_content}</span>
                                                </div>
                                            <p>${comment.content}</p>
                                            <a class='comment-reply-link btn-reply' href="#commentForm" data-comment-id="${comment.id}" data-comment-username="${comment.author}" title="Ответить на комментарий"><i class="bi-reply-fill"></i></a>
                                        </div>
                                        <div class="clear"></div>
                                    </div>
                                </li>`;

        if (comment.is_child) {
            document.querySelector(`#li-comment-${comment.parent_id}`).insertAdjacentHTML("beforeend", commentChildTemplate);
        }
        else {
            document.querySelector('.nested-comments').insertAdjacentHTML("beforeend", commentTemplate)
        }
        commentForm.reset()
        commentFormSubmit.disabled = false;
        commentFormSubmit.innerText = "Добавить комментарий";
        commentFormParentInput.value = null;
        replyUser();
    }
    catch (error) {
        console.log(error)
    }
}