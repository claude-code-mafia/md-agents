# MD Agents Documentation Site

This is the documentation site for MD Agents, built with Jekyll for GitHub Pages.

## Local Development

```bash
# Install dependencies
bundle install

# Run local server
bundle exec jekyll serve

# View at http://localhost:4000/claude-agents/
```

## Deployment

The site automatically deploys to GitHub Pages when pushed to the `gh-pages` branch.

```bash
# Build the site
bundle exec jekyll build

# Deploy to GitHub Pages
# (Assumes you have gh-pages branch set up)
git subtree push --prefix docs-site/_site origin gh-pages
```

## Structure

- `/` - Homepage
- `/quickstart/` - Getting started guide  
- `/examples/` - Example agents and patterns
- `/docs/` - Core documentation
- `/api/` - API reference
- `/_layouts/` - Page templates
- `/_includes/` - Reusable components
- `/assets/` - CSS, JS, images

## Adding Content

1. Create a new `.md` file in the appropriate directory
2. Add front matter:
   ```yaml
   ---
   layout: docs
   title: Your Page Title
   description: Brief description
   ---
   ```
3. Write content in Markdown
4. Add to navigation in `_includes/sidebar.html` if needed

## Styling

The site uses a minimal, documentation-focused design inspired by OpenAI's agent SDK docs. Key design principles:

- Clean, readable typography
- Code-first examples
- Minimal visual clutter
- Mobile responsive
- Fast loading