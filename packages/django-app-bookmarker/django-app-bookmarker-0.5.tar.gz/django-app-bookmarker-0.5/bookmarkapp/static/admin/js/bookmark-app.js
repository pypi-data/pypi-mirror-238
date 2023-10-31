class Bookmarker {
    constructor(ref_id) {
        this.ref = document.getElementById(ref_id);
        this.key_of_items = 'bookmarks';
        this.items = this.getBookmarks();
        
    }

    updateRemoveButtonListenners() {
        const buttons_bookmarked = document.querySelectorAll('.bookmarked-item');
        buttons_bookmarked.forEach(button=>{
            button.addEventListener('click', (e)=>{
                const data = e.target.dataset;
                this.removeFromBookmark(data.name);
            });
        });
    }

    renderBookmarks() {
        let innerHTML = ""
        this.items.forEach((e) => {
            innerHTML += `
            <tr>
                <th>
                    <a href="${e.admin_url}">${e.name}</a>
                </th>
                <td class="bookmarked-item">
                    Remove &#10134;
                </td>
            </th>
            `
        });
        this.ref.innerHTML = innerHTML
    }

    updateBookmarks(items) {
        this.items = items;
        localStorage.setItem(this.key_of_items, JSON.stringify(this.items));
        this.renderBookmarks();
        this.updateRemoveButtonListenners()
    }

    getBookmarks() {
        let bookmarks = localStorage.getItem(this.key_of_items);
        if (bookmarks == null) {
            bookmarks = [];
            localStorage.setItem(this.key_of_items, JSON.stringify(bookmarks));
        }
        return JSON.parse(bookmarks);
    }

    addToBookmark(admin_url, name, object_name) {
        const bookmarks = this.items;
        const index = bookmarks.findIndex(item=>item.name==name);
        if (index == -1) {
            bookmarks.push({admin_url, name, object_name});
            this.updateBookmarks(bookmarks);
        }
        else {
            this.removeFromBookmark(name);
        }
    }


    removeFromBookmark(name) {
        const bookmarks = this.items;
        const index = bookmarks.findIndex(item=>item.name==name);
        bookmarks.splice(index, 1);
        this.updateBookmarks(bookmarks);
    }
}


document.addEventListener('DOMContentLoaded', (e)=>{

    const bookmarker = new Bookmarker('bookmark-apps');
    const buttons = document.querySelectorAll('.bookmark-item');

    bookmarker.renderBookmarks();
    bookmarker.updateRemoveButtonListenners();

    buttons.forEach(button=>{
        button.addEventListener('click', (e)=>{
            const data = e.target.dataset;
            bookmarker.addToBookmark(data.admin_url, data.name, data.object_name);
        });
    });

    

});