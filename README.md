# Resume Optimizer  

This is a FastAPI application using DeepSeek-R1-Distill-Qwen-1.5B to optimize resume bullet points based on job descriptions.


## Project Structure

```
resume_rag
├── app
│   ├── main.py                          # Entry point of the FastAPI application
│   ├── api
│   │   └── v1
│   │       └── endpoints
│   │           └── resume_optimizer.py  # API endpoints for the resume resource
│   ├── core
│   │   └── config.py                    # Configuration settings
│   ├── models
│   │   └── llm_manager.py               # LLM management logic
│   │   └── resume_optimizer.py          # Data models
│   ├── schemas
│   │   └── resume_optimizer.py          # Pydantic schemas for validation
│   └── crud
│       └── example.py                   # CRUD operations for the resume resource
├── requirements.txt                     # Project dependencies
├── Dockerfile                           # Docker image instructions
└── README.md                            # Project documentation
```


## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/mwilliams619/resume_rag
   cd resume_rag
   ```

2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## Usage

Access the API at `http://127.0.0.1:8000`. You can also view the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Contributions

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

Please make sure your code follows the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
