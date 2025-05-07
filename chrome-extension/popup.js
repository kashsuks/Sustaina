document.addEventListener('DOMContentLoaded', function() {
    const statusEl = document.getElementById('status');
    const productInfoEl = document.getElementById('product-info');
    const productNameEl = document.getElementById('product-name');
    const brandNameEl = document.getElementById('brand-name');
    const productPriceEl = document.getElementById('product-price');
    const analysisDetailsEl = document.getElementById('analysis-details');
    const analysisContentEl = document.getElementById('analysis-content');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    function analyzeCurrentPage() {
      statusEl.className = 'status loading';
      statusEl.textContent = 'Analyzing current page...';
      productInfoEl.style.display = 'none';
      analysisDetailsEl.style.display = 'none';
      
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const activeTab = tabs[0];
        
        chrome.tabs.sendMessage(activeTab.id, {action: "analyze"}, function(response) {
          if (chrome.runtime.lastError) {
            statusEl.className = 'status not-clothing';
            statusEl.textContent = 'Error: Could not analyze this page. Please refresh and try again.';
            return;
          }
          
          if (!response) {
            statusEl.className = 'status not-clothing';
            statusEl.textContent = 'Error: No response from page. Please refresh and try again.';
            return;
          }
          
          if (!response.isClothingWebsite) {
            statusEl.className = 'status not-clothing';
            statusEl.textContent = 'This does not appear to be a clothing website.';
            return;
          }
          
          productNameEl.textContent = response.productName || 'Unknown';
          brandNameEl.textContent = response.brandName || 'Unknown';
          productPriceEl.textContent = response.productPrice || 'Unknown';
          productInfoEl.style.display = 'block';
          
          let statusClass = '';
          switch (response.ethicalRating) {
            case 'ethical':
              statusClass = 'ethical';
              statusEl.textContent = '✅ This product appears to be ethically sourced';
              break;
            case 'questionable':
              statusClass = 'questionable';
              statusEl.textContent = '⚠️ This product has questionable ethical sourcing';
              break;
            case 'unethical':
              statusClass = 'unethical';
              statusEl.textContent = '❌ This product appears to be unethically sourced';
              break;
            default:
              statusClass = 'questionable';
              statusEl.textContent = '❓ Could not determine ethical sourcing';
          }
          statusEl.className = `status ${statusClass}`;
          
          if (response.analysisDetails && response.analysisDetails.length > 0) {
            let detailsHtml = '<ul>';
            response.analysisDetails.forEach(detail => {
              detailsHtml += `<li>${detail}</li>`;
            });
            detailsHtml += '</ul>';
            analysisContentEl.innerHTML = detailsHtml;
            analysisDetailsEl.style.display = 'block';
          }
        });
      });
    }
    
    analyzeCurrentPage();
    
    analyzeBtn.addEventListener('click', analyzeCurrentPage);
  });