# CRITICAL ISSUES FOUND IN APP.PY

## 1. Duplicate Model Definition
**ServiceBooking** is defined TWICE (lines 82 and  244)!

### First Definition (Line 82) - OLD
- References: customer_id, technician_id
- Fields: date, time, status, vehicle_info, service_type, issues_reported
- Missing: booking_id, payment tracking

### Second Definition (Line 244) - NEW/BETTER
-  Has: booking_id, customer details, vehicle details, service_id
- Has: payment_status, total_amount
- More complete for web bookings

**DECISION**: 
- Remove FIRST definition (line 82-92)
- Keep SECOND definition (line 244-263) as it's more complete
- OR rename first to `TechnicianAppointment` if needed for internal tracking

## 2. Old Model References Still in Code
These models DON'T EXIST but are referenced in functions:

- **PatientProfile** → Should be **CustomerProfile**  
- **DoctorProfile** → Should be **TechnicianProfile**
- **Appointment** → Should be **ServiceBooking**  
- **DoctorReview** → Should be **TechnicianReview**

### Locations to Fix:
1. Line 410: `patient_email = appointment.patient.user.email`
2. Line 414: `appointment.patient.name`
3. Line 417: `appointment.doctor.name`
4. Line 418: `appointment.doctor.specialization`
5. Line 439-440: `calculate_doctor_rating(doctor_id)` and `DoctorReview.query`
6. Lines 452-458: get_dashboard_stats() function
7. Line 467: `DoctorReview.rating`
8. Line 618: `role='patient'`
9. Line 622: `PatientProfile(...)`
10. Lines 640-643: `user.role == 'doctor'`, `doctor_dashboard`, `patient_dashboard`
11. Lines 711-769: All patient/doctor admin routes
12. Lines 771-828: add_doctor, edit_doctor, delete_doctor routes
13. Lines 831-900+: patient and doctor dashboard routes

## 3. Helper Functions Need Update
- Line ~380: `is_patient()` → `is_customer()`
- Line ~383: (add) `is_technician()`  
- Remove references to undefined models

## 4.  Database Table Names
Need to ensure consistency:
- `service_booking` (✓ correct)
- `customer_profile` (✓ correct)
- `technician_profile` (✓ correct)
- `technician_review` (✓ correct)

## RECOMMENDATION
Create a CLEAN app.py with:
1. Only ONE ServiceBooking model
2. All old model references updated
3. All route names updated to automotive  terms
4. All function names updated

This requires ~100+ line changes in app.py alone.
