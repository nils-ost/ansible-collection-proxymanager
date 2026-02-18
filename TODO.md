# TODO

## Future Enhancements

### Add support for locations parameter
- The `locations` parameter in the NPM API is a complex array of objects that allows configuring custom location blocks
- This feature should allow users to define custom location paths with specific configurations
- Example structure:
  ```json
  "locations": [
    {
      "path": "/api",
      "forward_scheme": "http",
      "forward_host": "backend.internal",
      "forward_port": 8080
    }
  ]
  ```
- Implementation considerations:
  - Define a proper schema for location objects
  - Add validation for location parameters
  - Update documentation with examples
  - Ensure backward compatibility
