// src/themes/HighTechNeon/GetItems.js

/**
 * Safely retrieves an array of items from a given data object,
 * handling differences in structure (e.g., data?.items vs data?.items?.data).
 *
 * @param {Object} data - The section's data object (from the CMS).
 * @return {Array} An array of items, or an empty array if none found.
 */
export function getItemData(data) {
    if (!data) {
      console.warn("getItemData: No data provided.");
      return [];
    }
  
    // If there's a nested structure like data.items.data, return that
    if (data.items && Array.isArray(data.items.data)) {
      return data.items.data;
    }
  
    // Else if data.items is already an array
    if (data.items && Array.isArray(data.items)) {
      return data.items;
    }
  
    // Or if the top-level data is itself an array
    if (Array.isArray(data)) {
      return data;
    }
  
    // Fallback: no items found
    console.warn("getItemData: No items found in the provided data.");
    return [];
  }
  