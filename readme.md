# TodoPro - Advanced Todo Application

## Overview
TodoPro is a full-featured todo application with task management, analytics, and user authentication. The application features a modern UI with responsive design and comprehensive task management capabilities.

## Features
- **Task Management**: Create, edit, delete, and mark tasks as complete
- **Priority Levels**: Low, Medium, High, and Urgent priority options
- **Analytics Dashboard**: Track completion rates and productivity metrics
- **User Authentication**: Secure login and registration system
- **Responsive Design**: Works on all device sizes
- **Data Persistence**: Tasks stored in browser's local storage

## Pages
- **Dashboard** (`index.html`): Main task management interface
- **All Tasks** (`all-tasks.html`): Dedicated task management page
- **Analytics** (`analytics.html`): Productivity insights and metrics

## Deployment on Vercel

### Method 1: Deploy with Vercel CLI

1. Install Vercel CLI globally:
```bash
npm i -g vercel
```

2. Navigate to your project directory:
```bash
cd todoApp
```

3. Deploy to Vercel:
```bash
vercel
```

Follow the prompts to configure your deployment:
- Set the root directory as `frontend`
- Configure build settings if needed
- Deploy!

### Method 2: Deploy via Vercel Dashboard

1. Push your code to a GitHub/GitLab/Bitbucket repository
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Import your repository
5. In the configuration:
   - Framework Preset: `Other Static Generate`
   - Build Command: `echo "No build needed"`
   - Output Directory: `frontend`
   - Development Command: `skip`
6. Click "Deploy"

### Method 3: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/todoApp)

## Configuration Notes

### Frontend
- The application uses browser's local storage for data persistence
- All pages are located in the `frontend` directory
- Authentication is simulated with localStorage (for demo purposes)

### Backend (Optional)
For full backend functionality, you can deploy the FastAPI backend separately:
- The backend is located in the `backend` directory
- It uses FastAPI with SQLModel and SQLite
- API endpoints follow the specification in the `specs` directory

## Environment Variables (if using backend)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **Backend**: Python, FastAPI, SQLModel, SQLite
- **Authentication**: JWT-based system
- **UI Components**: Font Awesome icons

## Local Development
To run the application locally:
1. Navigate to the `frontend` directory
2. Serve the files using any HTTP server:
   ```bash
   npx http-server
   ```
3. Open the provided URL in your browser

## Support
For support, please contact the development team or submit an issue on the repository.

## License
This project is licensed under the MIT License.