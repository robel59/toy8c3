import os
import json
from bs4 import BeautifulSoup
import sys
from imageupload import *  # Import your image upload function

# Replace with your actual model

text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']

def add_unique_id(tag, existing_ids):
    base_id = tag.name
    index = 1
    new_id = f"{base_id}_{index}"
    while new_id in existing_ids:
        index += 1
        new_id = f"{base_id}_{index}"
    existing_ids.append(new_id)
    return new_id

def add_ids_to_tags(soup, tag_names, existing_ids):
    for tag_name in tag_names:
        tags = soup.find_all(tag_name)
        for tag in tags:
            tag_id = add_unique_id(tag, existing_ids)
            tag['id'] = tag_id

def update_html_template(template_content, generated_js_code):
    soup = BeautifulSoup(template_content, 'html.parser')

    # Add {% load static %} and {% load custom_tags %} at the beginning
    load_static_tag = soup.new_tag('script')
    load_static_tag.string = "{% load static %}"
    load_custom_tags_tag = soup.new_tag('script')
    load_custom_tags_tag.string = "{% load custom_tags %}"
    soup.head.insert(0, load_static_tag)
    soup.head.insert(1, load_custom_tags_tag)

    # Add <script>var jsonDataww = {{ json_data|safe }};</script> at the top
    json_script_tag = soup.new_tag('script')
    json_script_tag.string = "var jsonDataww = {{ json_data|safe }};"
    soup.head.insert(2, json_script_tag)

    # Add {% render_login_modal logstat chat_id %}
    render_login_modal_tag = soup.new_tag('div')
    render_login_modal_tag.string = "{% render_login_modal logstat chat_id %}"
    soup.body.insert_before(render_login_modal_tag)

    # Replace static file paths with {% static %} template tags
    for link_tag in soup.find_all('link'):
        if 'href' in link_tag.attrs:
            href = link_tag['href']
            if href.startswith('/static/'):
                link_tag['href'] = f"{{% static '{href[len('/static/'):]} %}}"
            else:
                link_tag['href'] = f"{{% static '{href}' %}}"

    for script_tag in soup.find_all('script'):
        if 'src' in script_tag.attrs:
            src = script_tag['src']
            if src.startswith('/static/'):
                script_tag['src'] = f"{{% static '{src[len('/static/'):]} %}}"
            else:
                script_tag['src'] = f"{{% static '{src}' %}}"

    # Replace href attributes with {% static %} template tags
    for link_tag in soup.find_all('link', href=True):
        if link_tag['href'].startswith('assets/'):
            link_tag['href'] = f"{{% static '{link_tag['href']}' %}}"

    # Replace src attributes with {% static %} template tags
    for script_tag in soup.find_all('script', src=True):
        if script_tag['src'].startswith('assets/'):
            script_tag['src'] = f"{{% static '{script_tag['src']}' %}}"

    # Add <script src="{% static 'webfunction.js' %}"></script> before </body>
    script_tag = soup.new_tag('script', src="{% static 'webfunction.js' %}")
    soup.body.append(script_tag)

    # Remove text content from specific tags as before
    text_tags0 = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']

    for tag in soup.find_all(text_tags0):
        tag.string = ""

    generated_js_tag = soup.new_tag('script')
    generated_js_tag.string = generated_js_code
    soup.body.append(generated_js_tag)

    return str(soup)


def generate_json_data(soup, tag_names):
    json_data = {}

    for tag_name in tag_names:
        if tag_name == 'a':
            link_tags = soup.find_all('a')

            # Extract and print the links and icons
            for link in link_tags:
                if 'id' in link.attrs:
                    tag_id = link['id']
                    href = link.get('href') 
                    # Check if the link contains an icon represented as an HTML element
                    icon_tag = link.find('i') or link.find('span') or link.find('svg')
                    if href and icon_tag:
                        icon_html = icon_tag.prettify()  # Get the HTML of the icon
                        text = link.get_text().strip()  # Get the text within the <a> tag
                        print(f"Link: {href}, Text: {text}, Icon: {icon_html}")
                        link_a = {}
                        link_a['link'] = href
                        link_a['text'] = f"{text}{icon_html}"
                        json_data[tag_id] = link_a

        else:
            tags = soup.find_all(tag_name)
            for tag in tags:
                if 'id' in tag.attrs:
                    tag_id = tag['id']
                    json_data[tag_id] = tag.get_text().strip()

    return json_data

def process_html_file(input_html_path, existing_ids):
    with open(input_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # Adding IDs to text-containing tags
    add_ids_to_tags(soup, text_tags, existing_ids)

    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        impath = os.path.dirname(input_html_path)
        img_path = os.path.join(impath, img_tag['src'])
        image_id = upload_image_to_model(img_path)
        img_tag['src'] = f"{{% get_image_url {image_id} %}}"

    generated_js_code = """
    document.addEventListener('DOMContentLoaded', function () {
        // Iterate over each key in the JSON data
        for (var key in jsonDataww) {
            if (jsonDataww.hasOwnProperty(key)) {
                var element = document.getElementById(key);
                if (element) {
                    if(key.startsWith("a")){
                        element.href = jsonDataww[key['link']];
                    }else{
                        element.textContent = jsonDataww[key];
                    }
                }
            }
        }
    });
    """

    updated_html = update_html_template(str(soup), generated_js_code)

    # Save the updated HTML back to the file
    with open(input_html_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)

    data = generate_json_data(soup, text_tags)
    json_data_str = json.dumps(data)
    upload_json_other(json_data_str)

    print(f"Updated HTML with IDs written to {input_html_path}")


def process_html_files_in_directory(directory):
    existing_ids = extract_json_keys()

    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            input_html_path = os.path.join(directory, filename)
            process_html_file(input_html_path, existing_ids)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py /path/to/html/directory")
        sys.exit(1)

    html_directory = sys.argv[1]
    process_html_files_in_directory(html_directory)
