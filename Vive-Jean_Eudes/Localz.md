## 3. Localz

A handful of issues were present on the website while it was available. The connection with the google account was disabled, and only manual account were working. While testing the various features, the site seems to be a bit slow with many requests having CORS-related issues.
We noticed that all the user have the ability to modify a broad range of data, which caused many confusion due to other group testing the product at the same time. Despite frequent disconnections, we were able to ensure most features were still working with a small subset of exceptions:

- rides description are not saved properly, causing them to be lost after submitted
- conversation were crashing the tab due to an infinite loop so all the related features could not be tested appropriately
- the filter button does not work on some pages such as product views, where it appear to do nothing
- the website was not fully responsive, with text overflowing