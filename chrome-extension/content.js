chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "analyze") {
      const analysis = analyzeCurrentPage()
      sendResponse(analysis)
    }
    return true
  })
  
  function isClothingWebsite() {
    const clothingKeywords = [
      "clothing",
      "fashion",
      "apparel",
      "wear",
      "outfit",
      "dress",
      "shirt",
      "pants",
      "jeans",
      "sweater",
      "jacket",
      "coat",
      "shoes",
      "boots",
      "t-shirt",
      "hoodie",
      "sweatshirt",
      "skirt",
      "blouse",
      "suit",
    ]
  
    const pageText = document.body.innerText.toLowerCase()
    const metaTags = document.querySelectorAll('meta[name="keywords"], meta[name="description"]')
    let metaContent = ""
  
    metaTags.forEach((tag) => {
      metaContent += " " + (tag.getAttribute("content") || "").toLowerCase()
    })
  
    const url = window.location.href.toLowerCase()
    const urlContainsClothingTerms = clothingKeywords.some((keyword) => url.includes(keyword))
  
    const contentMatchCount = clothingKeywords.filter(
      (keyword) => pageText.includes(keyword) || metaContent.includes(keyword),
    ).length
  
    const commonRetailers = [
      "zara",
      "h&m",
      "uniqlo",
      "gap",
      "forever21",
      "nordstrom",
      "macys",
      "asos",
      "nike",
      "adidas",
      "patagonia",
      "everlane",
      "lululemon",
      "anthropologie",
      "urban outfitters",
      "old navy",
      "banana republic",
    ]
  
    const isKnownRetailer = commonRetailers.some(
      (retailer) =>
        url.includes(retailer) ||
        document.title.toLowerCase().includes(retailer) ||
        pageText.toLowerCase().includes(retailer),
    )
  
    return urlContainsClothingTerms || contentMatchCount >= 3 || isKnownRetailer
  }
  
  function extractProductInfo() {
    let productName = ""
    const possibleProductNameElements = [
      document.querySelector("h1"),
      document.querySelector(".product-title"),
      document.querySelector(".product-name"),
      document.querySelector('[data-testid="product-title"]'),
      document.querySelector('[class*="product-title"]'),
      document.querySelector('[class*="productTitle"]'),
      document.querySelector('[class*="product-name"]'),
      document.querySelector('[class*="productName"]'),
    ]
  
    for (const element of possibleProductNameElements) {
      if (element && element.textContent.trim()) {
        productName = element.textContent.trim()
        break
      }
    }
  
    let brandName = ""
    const possibleBrandElements = [
      document.querySelector(".brand"),
      document.querySelector(".brand-name"),
      document.querySelector('[data-testid="product-brand"]'),
      document.querySelector('[class*="brand-name"]'),
      document.querySelector('[class*="brandName"]'),
    ]
  
    for (const element of possibleBrandElements) {
      if (element && element.textContent.trim()) {
        brandName = element.textContent.trim()
        break
      }
    }
  
    if (!brandName) {
      const pageTitle = document.title
      const brandRegex = /by\s+([A-Za-z0-9\s&]+)|\|([A-Za-z0-9\s&]+)/i
      const match = pageTitle.match(brandRegex)
      if (match) {
        brandName = (match[1] || match[2]).trim()
      } else if (productName.includes("|")) {
        brandName = productName.split("|")[0].trim()
        productName = productName.split("|")[1].trim()
      }
    }
  
    let productPrice = ""
    const possiblePriceElements = [
      document.querySelector(".price"),
      document.querySelector(".product-price"),
      document.querySelector('[data-testid="product-price"]'),
      document.querySelector('[class*="product-price"]'),
      document.querySelector('[class*="productPrice"]'),
      document.querySelector('[class*="price"]'),
    ]
  
    for (const element of possiblePriceElements) {
      if (element && element.textContent.trim()) {
        productPrice = element.textContent.trim()
        break
      }
    }
  
    return {
      productName,
      brandName,
      productPrice,
    }
  }
  
  function extractProductDescription() {
    let description = ""
    const possibleDescElements = [
      document.querySelector(".product-description"),
      document.querySelector(".description"),
      document.querySelector('[data-testid="product-description"]'),
      document.querySelector('[class*="product-description"]'),
      document.querySelector('[class*="productDescription"]'),
      document.querySelector('[class*="description"]'),
    ]
  
    for (const element of possibleDescElements) {
      if (element && element.textContent.trim()) {
        description += " " + element.textContent.trim()
      }
    }
  
    const detailElements = document.querySelectorAll(
      '.product-details, .details, .specifications, [class*="product-details"], [class*="productDetails"]',
    )
    detailElements.forEach((element) => {
      description += " " + element.textContent.trim()
    })
  
    return description
  }
  
  function analyzeEthicalSourcing(brandName, productDescription) {
    const ethicalKeywords = [
      "sustainable",
      "ethical",
      "fair trade",
      "organic",
      "recycled",
      "eco-friendly",
      "environmentally friendly",
      "responsibly sourced",
      "green",
      "renewable",
      "biodegradable",
      "carbon neutral",
      "zero waste",
      "cruelty-free",
      "vegan",
      "locally made",
      "handmade",
      "artisan",
      "small batch",
      "living wage",
    ]
  
    const unethicalKeywords = [
      "fast fashion",
      "synthetic",
      "polyester",
      "acrylic",
      "nylon",
      "microplastic",
      "overseas factory",
      "mass produced",
      "cheap labor",
    ]

    const knownEthicalBrands = [
      "patagonia",
      "everlane",
      "eileen fisher",
      "reformation",
      "pact",
      "tentree",
      "outerknown",
      "allbirds",
      "kotn",
      "thought clothing",
      "people tree",
      "veja",
      "stella mccartney",
      "alternative apparel",
      "organic basics",
      "girlfriend collective",
      "nisolo",
      "able",
    ]

    const knownProblematicBrands = [
      "shein",
      "fashion nova",
      "forever 21",
      "boohoo",
      "pretty little thing",
      "missguided",
      "romwe",
      "zaful",
    ]

    const normalizedBrand = brandName.toLowerCase()

    if (knownEthicalBrands.some((brand) => normalizedBrand.includes(brand))) {
      return {
        ethicalRating: "ethical",
        analysisDetails: [
          `${brandName} is known for ethical and sustainable practices.`,
          "This brand has been recognized for its commitment to sustainability.",
          "The company typically uses eco-friendly materials and fair labor practices.",
        ],
      }
    }
  
    if (knownProblematicBrands.some((brand) => normalizedBrand.includes(brand))) {
      return {
        ethicalRating: "unethical",
        analysisDetails: [
          `${brandName} has been associated with fast fashion practices.`,
          "This brand has been reported to use unsustainable manufacturing methods.",
          "There have been concerns about labor practices in their supply chain.",
        ],
      }
    }

    const normalizedDesc = productDescription.toLowerCase()
    const ethicalMatches = ethicalKeywords.filter((keyword) => normalizedDesc.includes(keyword))
    const unethicalMatches = unethicalKeywords.filter((keyword) => normalizedDesc.includes(keyword))
  
    const analysisDetails = []
  
    if (ethicalMatches.length > 0) {
      analysisDetails.push(`Found positive indicators: ${ethicalMatches.join(", ")}`)
    }
  
    if (unethicalMatches.length > 0) {
      analysisDetails.push(`Found concerning indicators: ${unethicalMatches.join(", ")}`)
    }
  
    const certifications = [
      "GOTS",
      "Global Organic Textile Standard",
      "Fair Trade Certified",
      "OEKO-TEX",
      "Bluesign",
      "B Corp",
      "WRAP",
      "SA8000",
      "GRS",
      "Global Recycled Standard",
    ]
  
    const foundCertifications = certifications.filter(
      (cert) => productDescription.includes(cert) || document.body.innerText.includes(cert),
    )
  
    if (foundCertifications.length > 0) {
      analysisDetails.push(`Found certifications: ${foundCertifications.join(", ")}`)
    }

    let ethicalRating
    if (ethicalMatches.length > 2 || foundCertifications.length > 0) {
      ethicalRating = "ethical"
      analysisDetails.push("Multiple positive indicators suggest ethical sourcing.")
    } else if (unethicalMatches.length > 1) {
      ethicalRating = "unethical"
      analysisDetails.push("Multiple concerning indicators suggest questionable sourcing practices.")
    } else if (ethicalMatches.length > 0) {
      ethicalRating = "questionable"
      analysisDetails.push("Some positive indicators, but insufficient information for a definitive assessment.")
    } else {
      ethicalRating = "questionable"
      analysisDetails.push(
        "Insufficient information to determine ethical sourcing. Consider researching the brand further.",
      )
    }
  
    return {
      ethicalRating,
      analysisDetails,
    }
  }
  
  function analyzeCurrentPage() {
    const isClothing = isClothingWebsite()
  
    if (!isClothing) {
      return {
        isClothingWebsite: false,
      }
    }

    const productInfo = extractProductInfo()
    const productDescription = extractProductDescription()
    const ethicalAnalysis = analyzeEthicalSourcing(productInfo.brandName, productDescription)
  
    return {
      isClothingWebsite: true,
      ...productInfo,
      ...ethicalAnalysis,
    }
  }
  