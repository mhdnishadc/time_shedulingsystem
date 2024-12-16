import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

const Timeslotbooking = () => {
  const { id } = useParams();
  const [timeslots, setTimeslots] = useState([]);
  const [selectedTimeslot, setSelectedTimeslot] = useState(null);

  useEffect(() => {
    const fetchTimeslots = async () => {
      try {
        const response = await axios.get(`/routes/services/${id}/timeslots`);
        setTimeslots(response.data);
      } catch (error) {
        console.error("Error fetching timeslots:", error);
      }
    };
    fetchTimeslots();
  }, [id]);

  const handleBooking = async (timeslotId) => {
    try {
      await axios.post(
        "/routes/bookings",
        { timeslot_id: timeslotId },
        { headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` } }
      );
      alert("Booking confirmed!");
    } catch (error) {
      console.error("Error booking timeslot:", error);
    }
  };

  return (
    <div className="container my-5">
      <h2 className="text-center">Available Timeslots</h2>
      <div className="row">
        {timeslots.map((timeslot, index) => (
          <div key={index} className="col-md-4 mb-4">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{timeslot.day_of_week}</h5>
                <p className="card-text">
                  {timeslot.start_time} - {timeslot.end_time}
                </p>
                <p className="card-text">Vacancies: {timeslot.vacancies}</p>
                <button
                  className="btn btn-primary w-100"
                  onClick={() => handleBooking(timeslot.id)}
                >
                  Book Timeslot
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Timeslotbooking;