export async function GET() {
  return Response.json({
    status: 'healthy',
    message: 'Vibr API is running',
    version: '1.0.0'
  });
} 