# Vibr Cloud Deployment Guide

This guide covers deploying Vibr to the cloud so users can access it from any device without any local setup.

## 🚀 One-Click Deploy Options

### 1. Railway + Vercel (Recommended - Easiest)

**Perfect for users who want zero technical setup:**

1. **Fork this repository** to your GitHub account
2. **Deploy Backend to Railway**:
   - Visit [Railway](https://railway.app/) and sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repository
   - Railway will automatically detect the backend and deploy it
   - Add environment variables:
     - `ANTHROPIC_API_KEY`: Your Anthropic API key
     - `SECRET_KEY`: A secure random string (Railway can generate this)
3. **Deploy Frontend to Vercel**:
   - Visit [Vercel](https://vercel.com/) and sign up with GitHub
   - Click "New Project" → "Import Git Repository"
   - Select your forked repository
   - Set environment variable:
     - `NEXT_PUBLIC_API_URL`: Your Railway backend URL (e.g., `https://your-app.railway.app`)
   - Click "Deploy"

**Result**: Your app is live at `https://your-app.vercel.app` and accessible from any device!

### 2. Render (All-in-One)

**Deploy both frontend and backend on Render:**

1. **Fork this repository** to your GitHub account
2. **Visit [Render](https://render.com/)** and sign up
3. **Deploy Backend**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `vibr-backend`
     - **Environment**: `Docker`
     - **Branch**: `main`
   - Add environment variables:
     - `ANTHROPIC_API_KEY`: Your Anthropic API key
     - `SECRET_KEY`: A secure random string
4. **Deploy Frontend**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `vibr-frontend`
     - **Environment**: `Docker`
     - **Branch**: `main`
   - Add environment variable:
     - `NEXT_PUBLIC_API_URL`: Your backend URL (e.g., `https://vibr-backend.onrender.com`)

### 3. DigitalOcean App Platform

**Professional hosting with automatic scaling:**

1. **Fork this repository** to your GitHub account
2. **Visit [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)**
3. **Create App**:
   - Click "Create App" → "Create App from Source Code"
   - Connect your GitHub repository
   - DigitalOcean will automatically detect both services
4. **Configure Services**:
   - **Backend**: Set environment variables for API keys
   - **Frontend**: Set environment variable for backend URL
5. **Deploy**: Click "Create Resources"

## 🔧 Automatic Deployment (GitHub Actions)

The project includes automatic deployment via GitHub Actions:

1. **Fork the repository** to your GitHub account
2. **Set up secrets** in your GitHub repository:
   - Go to Settings → Secrets and variables → Actions
   - Add these secrets:
     - `RAILWAY_TOKEN`: Your Railway API token
     - `VERCEL_TOKEN`: Your Vercel API token
     - `VERCEL_ORG_ID`: Your Vercel organization ID
     - `VERCEL_PROJECT_ID`: Your Vercel project ID
     - `NEXT_PUBLIC_API_URL`: Your backend URL
3. **Push to main branch** - deployment happens automatically!

## 🌐 Domain Setup

### Custom Domain

1. **Purchase a domain** (e.g., from Namecheap, GoDaddy, or Google Domains)
2. **Configure DNS**:
   - For Vercel: Add CNAME record pointing to your Vercel app
   - For Railway: Add CNAME record pointing to your Railway app
3. **SSL certificate** is automatically provided by both platforms

### Subdomain Setup

- **Vercel**: Automatically provides `your-app.vercel.app`
- **Railway**: Automatically provides `your-app.railway.app`
- **Render**: Automatically provides `your-app.onrender.com`

## 🔒 Security Configuration

### Environment Variables

Always set these in production:

```env
# Backend (Railway/Render)
ANTHROPIC_API_KEY=your-anthropic-api-key
SECRET_KEY=your-secure-random-string
DATABASE_URL=postgresql://user:password@host:port/database

# Frontend (Vercel)
NEXT_PUBLIC_API_URL=https://your-backend-url.com
NEXT_PUBLIC_APP_NAME=Vibr
```

### CORS Settings

The backend automatically configures CORS for common domains. For custom domains, update the `ALLOWED_ORIGINS` environment variable:

```env
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 📊 Monitoring and Analytics

### Built-in Monitoring

- **Vercel Analytics**: Automatic performance monitoring
- **Railway Logs**: Real-time application logs
- **Health Checks**: Automatic health monitoring

### Custom Monitoring

Add monitoring services:

```yaml
# Add to your deployment configuration
monitoring:
  - service: sentry
    dsn: your-sentry-dsn
  - service: logrocket
    app_id: your-logrocket-app-id
```

## 🚀 Performance Optimization

### CDN and Edge Network

- **Vercel Edge Network**: Global CDN for frontend
- **Railway Edge**: Distributed backend deployment
- **Image Optimization**: Automatic image optimization

### Database Optimization

For production databases:

```env
# Use connection pooling
DATABASE_URL=postgresql://user:password@host:port/database?pool_size=20&max_overflow=30
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The included workflow automatically:

1. **Tests the code** on pull requests
2. **Deploys to staging** on push to develop branch
3. **Deploys to production** on push to main branch
4. **Runs health checks** after deployment

### Custom Workflows

Add custom deployment steps:

```yaml
# Add to .github/workflows/deploy.yml
- name: Run database migrations
  run: |
    # Add migration commands here

- name: Send deployment notification
  run: |
    # Add notification commands here
```

## 📈 Scaling

### Automatic Scaling

- **Vercel**: Automatic scaling based on traffic
- **Railway**: Automatic scaling with resource limits
- **Render**: Manual scaling with multiple instances

### Manual Scaling

For high-traffic applications:

```yaml
# Railway configuration
scaling:
  min: 1
  max: 10
  target_cpu: 70
```

## 🆘 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check build logs in your deployment platform
   - Verify all environment variables are set
   - Ensure dependencies are correctly specified

2. **Runtime Errors**:
   - Check application logs
   - Verify database connections
   - Check API key validity

3. **CORS Errors**:
   - Verify `ALLOWED_ORIGINS` includes your frontend domain
   - Check that frontend URL is correctly set in backend

### Debug Commands

```bash
# Check deployment status
railway status
vercel ls

# View logs
railway logs
vercel logs

# Test endpoints
curl https://your-backend-url.com/health
curl https://your-frontend-url.com
```

## 💰 Cost Optimization

### Free Tiers

- **Vercel**: Free tier includes 100GB bandwidth/month
- **Railway**: Free tier includes $5 credit/month
- **Render**: Free tier includes 750 hours/month

### Production Scaling

For production applications:

- **Vercel Pro**: $20/month for unlimited bandwidth
- **Railway**: Pay-as-you-use pricing
- **Render**: $7/month per service

## 📞 Support

For deployment issues:

1. **Check platform documentation**:
   - [Vercel Docs](https://vercel.com/docs)
   - [Railway Docs](https://docs.railway.app/)
   - [Render Docs](https://render.com/docs)

2. **Review logs** for error messages

3. **Verify environment variables** are correctly set

4. **Test locally first** before deploying

---

**Happy Deploying!** Your users will be able to access Vibr from any device without any technical setup! 🚀 