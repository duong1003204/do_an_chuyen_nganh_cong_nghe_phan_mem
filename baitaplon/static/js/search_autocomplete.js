// Đảm bảo code chạy sau khi DOM (và jQuery) đã tải
$(document).ready(function() {
    var searchInput = $('#navbar-search-input'); // Lấy input
    var suggestionsBox = $('#search-suggestions'); // Lấy div rỗng
    
    // Lấy URL từ thuộc tính 'data-ajax-url' chúng ta đặt trong navbar.html
    var searchUrl = searchInput.data('ajax-url'); 

    searchInput.on('keyup', function() {
        var query = $(this).val();
        
        // Chỉ tìm khi gõ 2 ký tự trở lên
        if (query.length < 2) { 
            suggestionsBox.empty().hide();
            return;
        }

        // Gửi yêu cầu AJAX
        $.ajax({
            url: searchUrl,
            data: { 'timkiem': query },
            dataType: 'json',
            success: function(data) {
                suggestionsBox.empty().show(); // Xóa cũ, hiện box
                
                if (data.results && data.results.length > 0) {
                    $.each(data.results, function(index, item) {
                        // Tạo item gợi ý
                        var suggestionItem = `
                            <a href="${item.url}" class="list-group-item list-group-item-action d-flex align-items-center">
                                <img src="${item.image}" alt="" style="width: 40px; height: 40px; object-fit: cover; margin-right: 10px; border-radius: 4px;">
                                <span>${item.name}</span>
                            </a>
                        `;
                        suggestionsBox.append(suggestionItem);
                    });
                } else {
                    // Thông báo nếu không tìm thấy
                    suggestionsBox.append('<span class="list-group-item list-group-item-light text-muted">Không tìm thấy sản phẩm...</span>');
                }
            }
        });
    });

    // Ẩn gợi ý khi click ra ngoài
    $(document).on('click', function(e) {
        if (!$(e.target).closest('#navbar-search-container').length) {
            suggestionsBox.empty().hide();
        }
    });
});