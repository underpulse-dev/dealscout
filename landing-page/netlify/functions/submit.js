exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }
  
  try {
    const data = JSON.parse(event.body);
    // Log submission (visible in Netlify Function logs)
    console.log('FORM_SUBMISSION:', JSON.stringify({
      type: data.formType || 'unknown',
      email: data.email || '',
      businessName: data['business-name'] || '',
      businessLocation: data['business-location'] || '',
      listingUrl: data['listing-url'] || '',
      reportType: data['report-type'] || '',
      timestamp: new Date().toISOString()
    }));
    
    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ success: true })
    };
  } catch (e) {
    console.log('FORM_ERROR:', e.message, 'Body:', event.body);
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid request' }) };
  }
};
