# Movie Scraper App - Project Plan

## Phase 1: Core UI Setup and Search Interface ✅
- [x] Create the main layout with Material Design 3 styling (header, search bar, content area)
- [x] Implement search input with JetBrains Mono font and red primary color
- [x] Add responsive grid layout for movie results display
- [x] Create movie card components with proper elevation (1dp at rest, 8dp on hover)
- [x] Add loading states and empty state messages

## Phase 2: Scraping Engine Integration ✅
- [x] Install required scraping libraries (requests, beautifulsoup4, lxml)
- [x] Create scraping module for fojik.com / fojic.site / mlwbd.is
- [x] Implement movie search functionality across multiple domains
- [x] Add error handling and timeout management
- [x] Create data models for movie results (title, URL, thumbnail, etc.)

## Phase 3: Download Link Extraction and UI ✅
- [x] Implement download link extraction from movie detail pages
- [x] Create download links display UI with Material Design cards
- [x] Add direct link generation functionality
- [x] Implement copy-to-clipboard feature for download links
- [x] Add manual URL input functionality for direct movie links
- [x] Create toast notifications for user feedback

## Phase 4: Inline Links and Homepage Latest Movies ✅
- [x] Remove modal popup and show download links inline in search results
- [x] Add expand/collapse functionality to movie cards
- [x] Automatically fetch direct download links when movie is expanded
- [x] Implement homepage latest movies scraper (fetch 10 latest from fojik.com)
- [x] Display latest movies grid on homepage with same inline link functionality
- [x] Add loading states for individual movie card link fetching
- [x] Fixed scraper to work with updated website structure (article.item instead of div.result-item)

## Phase 5: UI Verification
- [ ] Test homepage latest movies display
- [ ] Test search results with inline link expansion
- [ ] Test direct link auto-fetch and copy functionality
- [ ] Verify responsive layout and loading states
