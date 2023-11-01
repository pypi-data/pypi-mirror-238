/**
 * Sphinx `:download:` directive integration with PrismJS.
 *
 * Install the snippet by adding it to the sphinx conf.py configuration
 * as shown below:
 *
 *   prismjs_base = "//cdnjs.cloudflare.com/ajax/libs/prism/1.29.0"
 *
 *   html_css_files = [
 *       f"{prismjs_base}/themes/prism.min.css",
 *       f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.css",
 *       "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/css/sphinx_rtd_theme.css",
 *   ]
 *
 *   html_js_files = [
 *       f"{prismjs_base}/prism.min.js",
 *       f"{prismjs_base}/plugins/autoloader/prism-autoloader.min.js",
 *       f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.js",
 *       f"{prismjs_base}/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js",
 *       "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/js/download_adapter.js",
 *   ]
 *
 * @author Artur Barseghyan (https://github.com/barseghyanartur)
 * @url https://github.com/barseghyanartur/jsphinx
 * @version 1.3.4
 */

// ****************************************************
// ***************** Download listener ****************
// ****************************************************

document.addEventListener('DOMContentLoaded', function() {
    // Find all download links by their class
    let downloadLinks = document.querySelectorAll('.jsphinx-download a.reference.download.internal');

    downloadLinks.forEach(function(link, index) {
        // Create a unique id for the additional content div
        let contentID = 'additional-content-' + index;

        // Get the file extension and set language class
        let fileExtension = link.getAttribute('href').split('.').pop();
        let langClass = fileExtension === 'py' ? 'language-python' :
                        fileExtension === 'js' ? 'language-javascript' :
                        'language-plaintext';

        // Create a new div for the additional content
        let additionalContentDiv = document.createElement('div');
        additionalContentDiv.id = contentID;
        additionalContentDiv.style.display = 'none';

        // Create pre and code elements for syntax highlighting
        let preElement = document.createElement('pre');
        let codeElement = document.createElement('code');
        codeElement.classList.add(langClass);
        preElement.appendChild(codeElement);
        additionalContentDiv.appendChild(preElement);

        // Insert the additional content div after the link
        link.parentNode.insertBefore(additionalContentDiv, link.nextSibling);

        // Attach a click event to the download link
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Stop the link from being followed
            let additionalContent = document.getElementById(contentID).querySelector('code');

            if (additionalContentDiv.style.display === 'block') {
                additionalContentDiv.style.display = 'none';
            } else {
                // Check if content has been fetched
                if (!additionalContentDiv.classList.contains('fetched')) {
                    let retries = 3;
                    let url = link.getAttribute('href');
                    function fetchContent() {
                        // Fetch the content of the file and display it
                        let xhr = new XMLHttpRequest();
                        xhr.open('GET', url, true);
                        xhr.onreadystatechange = function() {
                            if (xhr.readyState === 4) {
                                if (xhr.status === 200) {
                                    additionalContent.textContent = xhr.responseText;
                                    Prism.highlightElement(additionalContent);
                                    additionalContentDiv.style.display = 'block';
                                    // Add fetched class
                                    additionalContentDiv.classList.add('fetched');
                                } else {
                                    additionalContent.textContent = 'Error fetching content.';
                                    additionalContentDiv.style.display = 'block';
                                }
                            }
                        };
                        xhr.send();
                    }
                    fetchContent();
                } else {
                    // Content has been fetched, just show it
                    additionalContentDiv.style.display = 'block';
                }
            }
        });
    });
});

// ****************************************************
// ****************** Toggle listeners ****************
// ****************************************************
document.addEventListener('DOMContentLoaded', function() {
    // Check if the HTML is under the 'jsphinx-toggle-emphasis' class
    const containers = document.querySelectorAll('.jsphinx-toggle-emphasis');

    containers.forEach((container) => {
        // Function to create a new div.highlight element with content from 'span.hll' elements
        function createNewCodeBlock(originalCodeBlock) {
            const spanElements = originalCodeBlock.querySelectorAll('span.hll');
            const newCodeBlock = document.createElement('div');
            newCodeBlock.classList.add('highlight');

            // Create a new pre element to hold the 'span.hll' elements
            const newPreElement = document.createElement('pre');

            spanElements.forEach((span) => {
                // Clone the 'span' element and its content
                const spanClone = span.cloneNode(true);
                newPreElement.appendChild(spanClone);
            });

            newCodeBlock.appendChild(newPreElement);
            return newCodeBlock;
        }

        // Function to toggle visibility of code blocks
        function toggleCodeBlocks(codeBlock1, codeBlock2, toggleLink) {
            console.log('codeBlock1');
            console.log(codeBlock1);
            console.log('codeBlock2');
            console.log(codeBlock2);
            const codeBlock1Style = getComputedStyle(codeBlock1);

            if (codeBlock1Style.display === 'none') {
                codeBlock1.style.display = '';
                codeBlock2.style.display = '';
                toggleLink.querySelector('em').textContent = 'Hide the full example'; // Update the text within <em>
            } else {
                codeBlock1.style.display = 'none';
                toggleLink.querySelector('em').textContent = 'Show the full example'; // Update the text within <em>
            }
        }

        // Add toggle links and create a new div.highlight element for each code block
        const codeBlocks = container.querySelectorAll('.highlight-python');

        codeBlocks.forEach((originalCodeBlock) => {
            // Create a new div.highlight element with content from 'span.hll' elements
            const newCodeBlock = createNewCodeBlock(originalCodeBlock);

            // Hide the original code block and show the new one
            originalCodeBlock.style.display = 'none';

            // Create the "See the full example" link with updated text within <em>
            const toggleLink = document.createElement('p');
            toggleLink.href = 'javascript:;';
            toggleLink.classList.add('toggle-link');
            toggleLink.innerHTML = '<em>Show the full example</em>&nbsp;<a href="javascript:;" class="reference download internal"><code class="xref download docutils literal notranslate"><span class="pre">here</span></code></a>';

            // Add a click event listener to the link to toggle code blocks
            toggleLink.addEventListener('click', (event) => {
                event.preventDefault(); // Prevent the link from navigating
                toggleCodeBlocks(originalCodeBlock, newCodeBlock, toggleLink);
            });

            // Wrap the link in a <p> element
            const linkContainer = document.createElement('p');
            linkContainer.appendChild(toggleLink);

            // Insert the link and the new code block as siblings
            originalCodeBlock.parentNode.insertBefore(linkContainer, originalCodeBlock.previousSibling);
            originalCodeBlock.parentNode.insertBefore(newCodeBlock, linkContainer);
        });
    });
});


// ****************************************************
// ******************* Toggle listener ****************
// ****************************************************
document.addEventListener('DOMContentLoaded', function() {
    // Check if the HTML is under the 'jsphinx-toggle-emphasis-replace' class
    const containers = document.querySelectorAll('.jsphinx-toggle-emphasis-replace');

    containers.forEach((container) => {
        // Function to create a new div.highlight element with content from 'span.hll' elements
        function createNewCodeBlock(originalCodeBlock) {
            const spanElements = originalCodeBlock.querySelectorAll('span.hll');
            const newCodeBlock = document.createElement('div');
            newCodeBlock.classList.add('highlight');

            // Create a new pre element to hold the 'span.hll' elements
            const newPreElement = document.createElement('pre');

            spanElements.forEach((span) => {
                // Clone the 'span' element and its content
                const spanClone = span.cloneNode(true);
                newPreElement.appendChild(spanClone);
            });

            newCodeBlock.appendChild(newPreElement);
            return newCodeBlock;
        }

        // Function to toggle visibility of code blocks
        function toggleCodeBlocks(codeBlock1, codeBlock2, toggleLink) {
            const codeBlock1Style = getComputedStyle(codeBlock1);

            if (codeBlock1Style.display === 'none') {
                codeBlock1.style.display = '';
                codeBlock2.style.display = 'none';
                toggleLink.querySelector('em').textContent = 'Hide the full example'; // Update the text within <em>
            } else {
                codeBlock1.style.display = 'none';
                codeBlock2.style.display = '';
                toggleLink.querySelector('em').textContent = 'Show the full example'; // Update the text within <em>
            }
        }

        // Add toggle links and create a new div.highlight element for each code block
        const codeBlocks = container.querySelectorAll('.highlight-python');

        codeBlocks.forEach((originalCodeBlock) => {
            // Create a new div.highlight element with content from 'span.hll' elements
            const newCodeBlock = createNewCodeBlock(originalCodeBlock);

            // Hide the original code block and show the new one
            originalCodeBlock.style.display = 'none';

            // Create the "See the full example" link with updated text within <em>
            const toggleLink = document.createElement('p');
            toggleLink.href = 'javascript:;';
            toggleLink.classList.add('toggle-link');
            toggleLink.innerHTML = '<em>Show the full example</em>&nbsp;<a href="javascript:;" class="reference download internal"><code class="xref download docutils literal notranslate"><span class="pre">here</span></code></a>';

            // Add a click event listener to the link to toggle code blocks
            toggleLink.addEventListener('click', (event) => {
                event.preventDefault(); // Prevent the link from navigating
                toggleCodeBlocks(originalCodeBlock, newCodeBlock, toggleLink);
            });

            // Wrap the link in a <p> element
            const linkContainer = document.createElement('p');
            linkContainer.appendChild(toggleLink);

            // Insert the link and the new code block as siblings
            originalCodeBlock.parentNode.insertBefore(linkContainer, originalCodeBlock.nextSibling);
            originalCodeBlock.parentNode.insertBefore(newCodeBlock, originalCodeBlock.nextSibling);
        });
    });
});
