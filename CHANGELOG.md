# Changelog

All notable changes to this project will be documented in this file.

## [v0.2.0-beta.1] - 2026-01-07

### Added
- **Multiple Data Loading Options**:
    - **File Upload**: Maintained and refined the existing Excel file upload.
    - **Archive Loading**: Fetch the latest public EM-DAT dataset from the UCLouvain Dataverse API.
    - **API Integration**: Structural support for fetching data directly via the EM-DAT API using an API key.
- **New Utilities**:
    - `utils/apiload.py`: Configuration and metadata for the EM-DAT API.
    - `utils/archload.py`: Configuration and metadata for the EM-DAT Archive.
- **Improvements Documentation**: Added `note.md` with suggestions for future performance and feature enhancements.

### Changed
- **UI/UX Enhancements**:
    - Refactored Home page with a radio button selection for loading methods.
    - Integrated `st.spinner` for better feedback during data loading.
    - Updated homepage instructions for all loading methods.
- **Filter Improvements**:
    - Enhanced filter synchronization: filters now reset correctly when switching datasets.
    - Standardized filter defaults and handling in `utils/filters.py`.

### Fixed
- Issue where start/end dates were not resetting correctly when switching data sources.
- Robustness in data loading: added better error handling for network requests and data processing.

### Technical
- Centralized data processing in `process_data` to ensure consistent session state management.
- Utilized `@st.cache_data` for all data loading functions to optimize performance.
- Standardized docstrings using the NumPy style.
- Added `requests` dependency to `requirements.txt`.
