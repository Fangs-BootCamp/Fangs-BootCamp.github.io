# FANGS Bootcamp

## Colors
For a simple implementation of color just wrap text in HTML tag:
```html
<any_name_for_tag_can_go_here> Random Text </any_name_for_tag_can_go_here>
```

Then anywhere in the markdown file include the css block:
```css
<style>
any_name_for_tag_can_go_here {
    color: your_color_here;
}
</style>
```

If you are wanting to seperate the styling from the markdown, you can create a `.css` file and then include it in the markdown
through this block of HTML:
```html
<link rel="stylesheet" href="location/of/css/file.css">
```

If you are wanting to create a block of text with color you can use an HTML `div` tag.
