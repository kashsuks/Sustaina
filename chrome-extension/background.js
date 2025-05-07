chrome.runtime.onInstalled.addListener(() => {
    console.log("Ethical Clothing Analyzer installed")
  })
  
  chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.active) {
      chrome.tabs.sendMessage(tabId, { action: "analyze" }, (response) => {
        if (response && response.isClothingWebsite) {
          chrome.storage.local.set({
            [`tab_${tabId}`]: response,
          })
  
          let iconPath = "images/icon_neutral.png"
          if (response.ethicalRating === "ethical") {
            iconPath = "images/icon_ethical.png"
          } else if (response.ethicalRating === "unethical") {
            iconPath = "images/icon_unethical.png"
          }
  
          chrome.action.setIcon({
            path: iconPath,
            tabId: tabId,
          })
        }
      })
    }
  })
  