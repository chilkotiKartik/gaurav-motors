# Gaurav Motors - Medical to Auto Workshop Migration Plan

## Overview
Converting the codebase from medical terminology (HMS - Hospital Management System) to automotive terminology (WIMS - Workshop & Inventory Management System).

## Critical Changes Needed

### 1. Database Models (app.py)
**OLD → NEW**
- `PatientProfile` → `CustomerProfile` ✅ (Already exists)
- `DoctorProfile` → `TechnicianProfile` ✅ (Already exists)
- `Appointment` → `ServiceBooking` ✅ (Already exists)
- `DoctorReview` → `TechnicianReview` ✅ (Already exists)

**Issue**: Old models are still being referenced in many functions even though new models exist!

### 2. User Roles
- `patient` → `customer`
- `doctor` → `technician`
- `admin` stays the same

### 3. Route Names to Update
- `/patient` → `/customer`
- `/patient/edit` → `/customer/edit`
- `/doctor` → `/technician`
- `/admin/add_patient` → `/admin/add_customer`
- `/admin/edit_patient/<id>` → `/admin/edit_customer/<id>`
- `/admin/delete_patient/<id>` → `/admin/delete_customer/<id>`
- `/admin/add_doctor` → `/admin/add_technician`
- `/admin/edit_doctor/<id>` → `/admin/edit_technician/<id>`
- `/admin/delete_doctor/<id>` → `/admin/delete_technician/<id>`
- `/book/<doctor_id>` → `/book/<technician_id>`
- `/appointment/<id>` → `/service/<id>`

### 4. Function Names to Update in app.py
- `is_patient()` → `is_customer()`
- `is_doctor()` → `is_technician()`
- `patient_dashboard()` → `customer_dashboard()`
- `patient_edit()` → `customer_edit()`
- `doctor_dashboard()` → `technician_dashboard()`
- `admin_add_patient()` → `admin_add_customer()`
- `admin_edit_patient()` → `admin_edit_customer()`
- `admin_delete_patient()` → `admin_delete_customer()`
- `add_doctor()` → `add_technician()`
- `admin_edit_doctor()` → `admin_edit_technician()`
- `admin_delete_doctor()` → `admin_delete_technician()`
- `send_appointment_confirmation()` → `send_service_confirmation()`
- `calculate_doctor_rating()` → `calculate_technician_rating()`

### 5. Template Files to Rename/Update
- `add_doctor.html` → `add_technician.html`
- `admin_add_patient.html` → `admin_add_customer.html`
- `admin_edit_patient.html` → `admin_edit_customer.html`
- `admin_edit_doctor.html` → `admin_edit_technician.html`
- `admin_patients.html` → `admin_customers.html`
- `doctor_dashboard.html` → `technician_dashboard.html`
- `doctor_reviews.html` → `technician_reviews.html`
- `list_doctors.html` → `list_technicians.html`
- `medical_history_form.html` → `vehicle_history_form.html`
- `medical_records.html` → `service_history.html`
- `patient_dashboard.html` → `customer_dashboard.html`
- `patient_edit.html` → `customer_edit.html`
- `appointment_detail.html` → `service_detail.html`
- `book.html` → Update content

### 6. Terminology Updates
**Medical → Automotive**
- Patient → Customer
- Doctor → Technic ian/Mechanic
- Appointment → Service Booking
- Diagnosis → Assessment/Work Performed
- Symptoms → Issues Reported
- Treatment → Service/Repair
- Medication → Parts Used
- Medical History → Service History
- Prescription → Parts Recommendation

## Implementation Strategy

### Phase 1: Core Models & Functions ✅
- Update all function references from old models to new models
- Update helper functions (is_patient → is_customer, etc.)
- Fix database queries

### Phase 2: Routes & Controllers  
- Update all route names
- Update function names
- Maintain backward compatibility with redirects if needed

### Phase 3: Templates
- Rename template files
- Update all template content
- Update form fields and labels

### Phase 4: Testing
- Test all routes
- Test all forms
- Verify database operations
-  Test user flows (customer, technician, admin)

## Notes
- The new models already exist (CustomerProfile, TechnicianProfile, ServiceBooking)
- Need to remove/update ALL references to old models
- Keep database migrations in mind
- Update error messages and flash messages
