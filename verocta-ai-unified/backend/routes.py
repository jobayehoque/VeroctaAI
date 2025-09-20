import os
import json
import logging
import random
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, send_file, send_from_directory, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename
from app import app
from auth import validate_user, create_user, get_current_user, require_admin
from models import create_report, get_reports_by_user, get_report_by_id, delete_report, init_sample_data
try:
    from database import db_service
except ImportError:
    db_service = None
from csv_parser import parse_csv_file, parse_csv_file_with_mapping
from gpt_utils import generate_financial_insights
from spend_score_engine import calculate_spend_score, get_score_label, get_score_color, get_enhanced_analysis
from pdf_generator import generate_report_pdf
from clone_verifier import verify_project_integrity

# Initialize sample data
init_sample_data()

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
ALLOWED_LOGO_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('outputs', exist_ok=True)

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_logo_file(filename):
    """Check if uploaded logo file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_LOGO_EXTENSIONS

# Legacy routes removed - now using React frontend with API endpoints

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'VeroctaAI Financial Intelligence Platform is running',
        'version': '2.0.0'
    })

@app.route('/verocta-logo.svg')
def serve_logo_svg():
    """Serve the logo SVG file"""
    try:
        frontend_build_dir = app.static_folder
        return send_from_directory(frontend_build_dir, 'verocta-logo.svg')
    except:
        # Fallback to assets directory
        return send_from_directory('static/assets/images', 'verocta-logo.png')

@app.route('/verocta-logo.png')
def serve_logo_png():
    """Serve the logo PNG file"""
    return send_from_directory('static/assets/images', 'verocta-logo.png')

# Authentication Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        user = validate_user(email, password)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        access_token = create_access_token(identity=email)

        return jsonify({
            'token': access_token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'role': user['role'],
                'company': user['company']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        company = data.get('company', 'Default Company')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400

        user = create_user(email, password, company)
        if not user:
            return jsonify({'error': 'User already exists'}), 409

        access_token = create_access_token(identity=email)

        return jsonify({
            'token': access_token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'role': user['role'],
                'company': user['company']
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Handle different user data formats
        created_at = user.get('created_at')
        if created_at:
            if hasattr(created_at, 'isoformat'):
                created_at = created_at.isoformat()
            else:
                created_at = str(created_at)
        else:
            created_at = None

        return jsonify({
            'user': {
                'id': str(user['id']),
                'email': user['email'],
                'role': user.get('role', 'user'),
                'company': user.get('company', 'Default Company'),
                'created_at': created_at
            }
        })
    except Exception as e:
        logging.error(f"Error in get_profile: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 401

# Reports API
@app.route('/api/reports', methods=['GET'])
@jwt_required()
def get_reports():
    """Get all reports for the current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Try database first
        if db_service and db_service.connected:
            db_reports = db_service.get_user_reports(str(user['id']))
            if db_reports:
                return jsonify({
                    'reports': db_reports,
                    'total': len(db_reports)
                })

        # Fallback to in-memory storage
        reports = get_reports_by_user(user['id'])
        return jsonify({
            'reports': [report.to_dict() for report in reports],
            'total': len(reports)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/<report_id>', methods=['GET'])
@jwt_required()
def get_report(report_id):
    """Get a specific report by ID"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Try database first
        if db_service and db_service.connected:
            try:
                db_reports = db_service.get_user_reports(str(user['id']))
                for db_report in db_reports:
                    if str(db_report.get('id')) == str(report_id):
                        return jsonify({'report': db_report})
                return jsonify({'error': 'Report not found'}), 404
            except Exception as db_error:
                logging.error(f"Database error: {str(db_error)}")
        
        # Fallback to in-memory storage
        try:
            report_id_int = int(report_id)
            report = get_report_by_id(report_id_int, user['id'])
            if not report:
                return jsonify({'error': 'Report not found'}), 404
            return jsonify({'report': report.to_dict()})
        except ValueError:
            return jsonify({'error': 'Invalid report ID format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/<report_id>', methods=['DELETE'])
@jwt_required()
def delete_report_endpoint(report_id):
    """Delete a specific report"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Try database first
        if db_service and db_service.connected:
            try:
                success = db_service.delete_report(report_id, str(user['id']))
                if success:
                    return jsonify({'message': 'Report deleted successfully'})
                else:
                    return jsonify({'error': 'Report not found or access denied'}), 404
            except Exception as db_error:
                logging.error(f"Database delete error: {str(db_error)}")
        
        # Fallback to in-memory storage
        try:
            report_id_int = int(report_id)
            success = delete_report(report_id_int, user['id'])
            if not success:
                return jsonify({'error': 'Report not found or access denied'}), 404
            return jsonify({'message': 'Report deleted successfully'})
        except ValueError:
            return jsonify({'error': 'Invalid report ID format'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/<report_id>/pdf', methods=['GET'])
@jwt_required()
def download_report_pdf(report_id):
    """Generate and download PDF report"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Try to get report from database first
        if db_service and db_service.connected:
            try:
                db_reports = db_service.get_user_reports(str(user['id']))
                report_data = None
                
                for db_report in db_reports:
                    if str(db_report.get('id')) == str(report_id):
                        report_data = db_report
                        break
                
                if not report_data:
                    return jsonify({'error': 'Report not found'}), 404
                
            except Exception as db_error:
                logging.error(f"Database error: {str(db_error)}")
                return jsonify({'error': 'Database error'}), 500
        else:
            # Fallback to in-memory storage
            try:
                report_id_int = int(report_id)
                report = get_report_by_id(report_id_int, user['id'])
                if not report:
                    return jsonify({'error': 'Report not found'}), 404
                report_data = report.to_dict()
            except ValueError:
                return jsonify({'error': 'Invalid report ID format'}), 400
        # Prepare analysis data from the report
        analysis_data = {
            'spend_score': report_data.get('spend_score', 75),
            'total_transactions': report_data.get('data', {}).get('transactions', 250),
            'total_amount': float(report_data.get('data', {}).get('total_amount', 45000.00)),
            'filename': report_data.get('title', f'Report {report_id}'),
            'suggestions': [
                {'text': rec, 'priority': 'High' if i < 2 else 'Medium' if i < 4 else 'Low'} 
                for i, rec in enumerate(report_data.get('insights', {}).get('recommendations', [
                    'Review recurring subscriptions for potential savings',
                    'Consider bulk purchasing for office supplies', 
                    'Implement expense approval workflow',
                    'Set up automated expense categorization',
                    'Review vendor contracts for better terms'
                ])[:5])
            ],
            'category_breakdown': report_data.get('data', {}).get('top_categories', {}),
            'score_label': get_score_label(report_data.get('spend_score', 75)),
            'score_color': get_score_color(report_data.get('spend_score', 75)),
            'waste_percentage': report_data.get('insights', {}).get('waste_percentage', 12.4),
            'duplicate_expenses': report_data.get('insights', {}).get('duplicate_expenses', 23),
            'spending_spikes': report_data.get('insights', {}).get('spending_spikes', 5),
            'savings_opportunities': report_data.get('insights', {}).get('savings_opportunities', 8)
        }

        # Generate category breakdown if not available
        if not isinstance(analysis_data['category_breakdown'], dict):
            total_amount = analysis_data['total_amount']
            analysis_data['category_breakdown'] = {
                'Software & SaaS': total_amount * 0.25,
                'Office Supplies': total_amount * 0.15,
                'Marketing': total_amount * 0.20,
                'Travel': total_amount * 0.15,
                'Professional Services': total_amount * 0.15,
                'Other': total_amount * 0.10
            }

        # Generate sample transactions for charts
        sample_transactions = [
            {
                'date': '2024-01-15',
                'amount': -500,
                'vendor': 'Office Depot',
                'category': 'Office Supplies'
            },
            {
                'date': '2024-01-20', 
                'amount': -1200,
                'vendor': 'Adobe',
                'category': 'Software & SaaS'
            },
            {
                'date': '2024-02-01',
                'amount': -800,
                'vendor': 'Google Ads',
                'category': 'Marketing'
            }
        ] * 50  # Multiply to get more sample data

        # Generate PDF
        from pdf_generator import generate_report_pdf
        pdf_path = generate_report_pdf(
            analysis_data,
            transactions=sample_transactions,
            company_name=user.get('company', 'Your Company')
        )

        if os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                as_attachment=True,
                download_name=f'verocta-report-{report_id}.pdf',
                mimetype='application/pdf'
            )
        else:
            return jsonify({'error': 'PDF generation failed'}), 500

    except Exception as e:
        logging.error(f"PDF download error: {str(e)}")
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

@app.route('/api/reports', methods=['POST'])
@jwt_required()
def create_report_endpoint():
    """Create a new report from uploaded data"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        title = data.get('title', f'Sample Report {datetime.now().strftime("%Y-%m-%d %H:%M")}')
        
        # Generate realistic sample data
        sample_data = {
            'transactions': random.randint(100, 800),
            'total_amount': random.randint(25000, 150000),
            'categories': random.randint(5, 15),
            'filename': f'{title.lower().replace(" ", "_")}.csv',
            'top_categories': ['Software & SaaS', 'Office Supplies', 'Marketing', 'Travel', 'Professional Services'],
            'upload_timestamp': datetime.now().isoformat()
        }
        
        # Generate realistic insights
        spend_score = random.randint(60, 95)
        insights_data = {
            'waste_percentage': max(5, 25 - (spend_score - 60) / 2),
            'duplicate_expenses': random.randint(10, 50),
            'spending_spikes': random.randint(2, 12),
            'savings_opportunities': random.randint(5, 15),
            'recommendations': [
                'Review subscription services for cost optimization',
                'Implement automated expense categorization',
                'Set up budget alerts for key spending categories',
                'Consider vendor consolidation opportunities',
                'Establish approval workflows for high-value transactions'
            ]
        }

        # Try to save to database first
        if db_service and db_service.connected:
            try:
                db_report = db_service.create_report(
                    user_id=str(user['id']),
                    title=title,
                    company=user.get('company', 'Default Company'),
                    data=sample_data,
                    spend_score=spend_score,
                    insights=insights_data
                )
                
                if db_report:
                    return jsonify({
                        'message': 'Report created successfully in database',
                        'report': {
                            'id': db_report['id'],
                            'title': db_report['title'],
                            'created_at': db_report['created_at'],
                            'spend_score': db_report['spend_score'],
                            'data': db_report['data'],
                            'insights': db_report['insights'],
                            'status': db_report['status']
                        }
                    }), 201
            except Exception as db_error:
                logging.error(f"Database creation failed: {str(db_error)}")

        # Fallback to in-memory storage
        report = create_report(title, user['id'], user['company'], sample_data, spend_score, insights_data)

        return jsonify({
            'message': 'Report created successfully',
            'report': report.to_dict()
        }), 201
        
    except Exception as e:
        logging.error(f"Report creation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def api_upload():
    """Enhanced API endpoint for CSV upload and analysis with mapping support"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    """Enhanced API endpoint for CSV upload and analysis with mapping support"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed.'}), 400

        # Get mapping information
        mapping_str = request.form.get('mapping', '{}')
        try:
            mapping = json.loads(mapping_str) if mapping_str else {}
        except json.JSONDecodeError:
            mapping = {}

        # Get company branding information
        company_name = request.form.get('company_name', '').strip()
        logo_path = None

        # Handle logo upload
        if 'companyLogo' in request.files:
            logo_file = request.files['companyLogo']
            if logo_file and logo_file.filename and allowed_logo_file(logo_file.filename):
                logo_filename = secure_filename(f"logo_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{logo_file.filename}")
                logo_path = os.path.join(app.config['UPLOAD_FOLDER'], logo_filename)
                logo_file.save(logo_path)
                logging.info(f"Logo uploaded: {logo_filename}")

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Parse CSV file with mapping
        try:
            if mapping and any(mapping.values()):
                logging.info(f"Using provided mapping: {mapping}")
                transactions = parse_csv_file_with_mapping(filepath, mapping)
            else:
                logging.info("No mapping provided, using auto-detection")
                transactions = parse_csv_file(filepath)
        except Exception as parse_error:
            logging.error(f"CSV parsing error: {str(parse_error)}")
            # Clean up uploaded file on error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({
                'error': f'Failed to parse CSV file: {str(parse_error)}',
                'details': 'Please check your column mapping and data format'
            }), 400

        if not transactions:
            return jsonify({
                'error': 'No valid transactions found in the CSV file',
                'details': 'Check that your amount column contains numeric values and the file has data rows'
            }), 400

        # Validate minimum transaction count
        if len(transactions) < 3:
            return jsonify({
                'error': f'Insufficient data for analysis. Found {len(transactions)} transactions, minimum 3 required.',
                'details': 'Upload a file with more transaction records for meaningful analysis'
            }), 400

        # Calculate enhanced spend score
        try:
            enhanced_analysis = get_enhanced_analysis(transactions)
        except Exception as analysis_error:
            logging.error(f"Analysis error: {str(analysis_error)}")
            return jsonify({
                'error': f'Analysis calculation failed: {str(analysis_error)}',
                'details': 'There may be an issue with the transaction data format'
            }), 500

        # Generate AI insights
        try:
            insights = generate_financial_insights(transactions)
        except Exception as insight_error:
            logging.warning(f"AI insights generation failed: {str(insight_error)}")
            # Provide fallback insights
            insights = {
                'recommendations': [
                    'Financial data processed successfully',
                    'Consider reviewing spending patterns for optimization opportunities',
                    'Implement budget tracking for better financial control'
                ],
                'priority_actions': ['Review high-value transactions', 'Categorize expenses']
            }

        # Calculate transaction summary
        total_amount = sum(float(t.get('amount', 0)) for t in transactions)

        # Prepare analysis results with enhanced data
        analysis_data = {
            'spend_score': enhanced_analysis['final_score'],
            'tier_info': enhanced_analysis['tier_info'],
            'score_breakdown': enhanced_analysis['score_breakdown'],
            'suggestions': insights,
            'total_transactions': len(transactions),
            'total_amount': total_amount,
            'enhanced_metrics': enhanced_analysis['transaction_summary'],
            'filename': filename,
            'green_reward_eligible': enhanced_analysis['tier_info'].get('green_reward_eligible', False),
            'company_name': company_name if company_name else None,
            'logo_path': logo_path if logo_path else None,
            'mapping_used': mapping
        }

        # Save JSON output
        output_json_path = os.path.join('outputs', 'verocta_analysis_output.json')
        with open(output_json_path, 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)

        # Generate PDF report with company branding
        try:
            pdf_path = generate_report_pdf(analysis_data, transactions, company_name, logo_path)
            pdf_available = os.path.exists(pdf_path)
        except Exception as pdf_error:
            logging.warning(f"PDF generation failed: {str(pdf_error)}")
            pdf_available = False

        # Prepare API response
        response_data = {
            'success': True,
            'filename': filename,
            'spend_score': enhanced_analysis['final_score'],
            'tier_info': enhanced_analysis['tier_info'],
            'score_breakdown': enhanced_analysis['score_breakdown'],
            'transaction_summary': enhanced_analysis['transaction_summary'],
            'ai_insights': insights,
            'analysis_timestamp': datetime.now().isoformat(),
            'company_name': company_name if company_name else None,
            'logo_path': logo_path if logo_path else None,
            'pdf_available': pdf_available,
            'mapping_used': mapping,
            'total_transactions_processed': len(transactions),
            'total_amount_analyzed': total_amount
        }

        return jsonify(response_data)

    except Exception as e:
        logging.error(f"API upload error: {str(e)}", exc_info=True)
        # Clean up uploaded files on error
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        if 'logo_path' in locals() and logo_path and os.path.exists(logo_path):
            os.remove(logo_path)
        return jsonify({
            'success': False,
            'error': f'Upload processing failed: {str(e)}',
            'details': 'Please try again or contact support if the issue persists'
        }), 500



@app.route('/api/report', methods=['GET'])
def api_download_report():
    """API endpoint to download latest PDF report"""
    try:
        pdf_path = os.path.join('outputs', 'verocta_report.pdf')

        if not os.path.exists(pdf_path):
            # Generate a sample PDF if none exists
            try:
                from pdf_generator import generate_report_pdf

                sample_analysis_data = {
                    'spend_score': 82,
                    'total_transactions': 350,
                    'total_amount': 67500.00,
                    'filename': 'Sample Financial Analysis',
                    'suggestions': [
                        {'text': 'Optimize subscription management to reduce recurring costs', 'priority': 'High'},
                        {'text': 'Implement automated expense categorization', 'priority': 'Medium'},
                        {'text': 'Review vendor contracts for better terms', 'priority': 'Medium'},
                        {'text': 'Set up budget alerts for key categories', 'priority': 'Low'}
                    ],
                    'category_breakdown': {
                        'Software & SaaS': 18500,
                        'Office & Equipment': 12000,
                        'Marketing & Advertising': 15000,
                        'Travel & Entertainment': 8000,
                        'Professional Services': 9000,
                        'Other': 5000
                    },
                    'score_label': 'Excellent',
                    'score_color': 'Green'
                }

                pdf_path = generate_report_pdf(
                    sample_analysis_data,
                    transactions=[],
                    company_name='VeroctaAI Demo'
                )

            except Exception as gen_error:
                logging.error(f"PDF generation error: {str(gen_error)}")
                return jsonify({'error': 'No PDF report available. Please analyze a CSV file first.'}), 404

        return send_file(
            pdf_path, 
            as_attachment=True, 
            download_name='verocta_financial_report.pdf',
            mimetype='application/pdf'
        )

    except Exception as e:
        logging.error(f"API report download error: {str(e)}")
        return jsonify({'error': f'Failed to download report: {str(e)}'}), 500

@app.route('/api/verify-clone', methods=['GET'])
def api_verify_clone():
    """API endpoint to check clone integrity status"""
    try:
        integrity_report = verify_project_integrity()

        # Simplified response for API
        response = {
            'status': integrity_report['status'],
            'message': integrity_report['message'],
            'files_checked': integrity_report['files_checked'],
            'files_matched': integrity_report['files_matched'],
            'files_modified': integrity_report['files_modified'],
            'files_missing': integrity_report['files_missing'],
            'total_deviations': len(integrity_report['deviations']),
            'timestamp': integrity_report['timestamp']
        }

        return jsonify(response)

    except Exception as e:
        logging.error(f"API clone verification error: {str(e)}")
        return jsonify({'error': f'Clone verification failed: {str(e)}'}), 500

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics for current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get reports for calculations
        reports = get_reports_by_user(user['id'])

        if reports:
            stats = {
                'total_reports': len(reports),
                'avg_spend_score': sum(r.spend_score for r in reports) // max(len(reports), 1),
                'total_savings': int(sum(r.data.get('total_amount', 0) for r in reports) * 0.15),
                'avg_waste_percentage': sum(r.insights.get('waste_percentage', 0) for r in reports) // max(len(reports), 1)
            }
        else:
            stats = {
                'total_reports': 0,
                'avg_spend_score': 0,
                'total_savings': 0,
                'avg_waste_percentage': 0
            }

        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/spend-score', methods=['GET'])
@jwt_required()
def get_spend_score():
    """Get latest spend score for current user"""
    try:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Try database first
        if db_service and db_service.connected:
            db_reports = db_service.get_user_reports(str(user['id']))
            if db_reports:
                latest_report = max(db_reports, key=lambda r: r.get('created_at', ''))
                return jsonify({
                    'score': latest_report.get('spend_score', 0),
                    'status': get_score_label(latest_report.get('spend_score', 0)),
                    'recommendations': latest_report.get('insights', {}).get('recommendations', []),
                    'report_id': latest_report.get('id'),
                    'created_at': latest_report.get('created_at')
                })

        # Fallback to in-memory storage
        reports = get_reports_by_user(user['id'])
        if not reports:
            # Return default data if no reports exist
            return jsonify({
                'score': 0,
                'status': 'No Data',
                'recommendations': ['Upload your first financial data to get started'],
                'report_id': None,
                'created_at': None
            })

        latest_report = max(reports, key=lambda r: r.created_at)

        return jsonify({
            'score': latest_report.spend_score,
            'status': get_score_label(latest_report.spend_score),
            'recommendations': latest_report.insights.get('recommendations', []),
            'report_id': latest_report.id,
            'created_at': latest_report.created_at.isoformat()
        })
    except Exception as e:
        logging.error(f"Error in get_spend_score: {str(e)}")
        # Return graceful fallback
        return jsonify({
            'score': 0,
            'status': 'No Data',
            'recommendations': ['Upload financial data to generate insights'],
            'report_id': None,
            'created_at': None
        })

@app.route('/api/docs')
def api_documentation():
    """API documentation endpoint"""
    docs = {
        "title": "VeroctaAI Financial Analysis API",
        "version": "2.0.0",
        "description": "AI-powered financial intelligence and SpendScore analysis platform",
        "base_url": request.host_url + "api/",
        "endpoints": {
            "POST /upload": {
                "description": "Upload CSV and trigger analysis",
                "parameters": {
                    "file": "CSV file (multipart/form-data)"
                },
                "response": "Analysis results with SpendScore and insights"
            },
            "GET /spend-score": {
                "description": "Return JSON of latest SpendScore metrics",
                "response": "SpendScore breakdown and tier information"
            },
            "GET /report": {
                "description": "Download latest PDF report",
                "response": "PDF file download"
            },
            "GET /verify-clone": {
                "description": "Returns sync integrity status",
                "response": "Clone verification report"
            },
            "GET /health": {
                "description": "Health check endpoint",
                "response": "Service status"
            },
            "GET /docs": {
                "description": "This API documentation",
                "response": "API documentation JSON"
            }
        },
        "authentication": {
            "type": "Bearer Token",
            "header": "Authorization: Bearer <token>",
            "note": "API key authentication coming in v2.1"
        },
        "supported_formats": [
            "QuickBooks CSV",
            "Wave Accounting CSV", 
            "Revolut CSV",
            "Xero CSV",
            "Generic transaction CSV"
        ]
    }

    return jsonify(docs)

# Serve main app
@app.route('/')
def serve_app():
    """Serve the main React application"""
    frontend_build_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
    return send_from_directory(frontend_build_dir, 'index.html')

# Serve static files
@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    # Check if it's an API route
    if filename.startswith('api/'):
        return "API route not found", 404

    # Check if the file exists in the frontend build directory
    frontend_build_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')

    if os.path.exists(os.path.join(frontend_build_dir, filename)):
        return send_from_directory(frontend_build_dir, filename)
    else:
        # For any other route, serve the main app
        return send_from_directory(frontend_build_dir, 'index.html')

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File is too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    # For API routes, return JSON error
    if request.path.startswith('/api/'):
        return jsonify({'error': 'API endpoint not found'}), 404
    # For other routes, serve main app
    frontend_build_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
    return send_from_directory(frontend_build_dir, 'index.html')

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    logging.error(f"Server error: {str(e)}")
    # For API routes, return JSON error
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    # For other routes, serve main app
    frontend_build_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
    return send_from_directory(frontend_build_dir, 'index.html')