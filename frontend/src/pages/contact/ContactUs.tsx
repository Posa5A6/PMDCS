import React, { useState } from "react";


import ContactCards from "./ContactCards";


interface FormData {
  name: string;
  email: string;
  phone: string;
  message: string;
  privacy: boolean;
}

interface Errors {
  name: string;
  email: string;
  message: string;
  phone: string;
  privacy: string;
}

interface ToastMessage {
  visible: boolean;
  message: string;
  success: boolean;
}


const ContactUs: React.FC = () => {

  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    phone: "",
    message: "",
    privacy: false,
  });

  const [errors, setErrors] = useState<Errors>({
    name: "",
    email: "",
    message: "",
    phone: "",
    privacy: "",
  });

  const [showToast, setShowToast] = useState<ToastMessage>({
    visible: false,
    message: "",
    success: true,
  });

  const validateForm = () => {
    const newErrors: Errors = {
      name: "",
      email: "",
      message: "",
      phone: "",
      privacy: "",
    };
    let isValid = true;

    if (!formData.name) {
      newErrors.name = "Name is required";
      isValid = false;
    }
    if (!formData.email) {
      newErrors.email = "Email is required";
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email address is invalid";
      isValid = false;
    }

    if (!formData.message) {
      newErrors.message = "Message is required";
      isValid = false;
    }

    if (!formData.phone || !/^\d{10}$/.test(formData.phone)) {
      newErrors.phone = "Enter a valid 10 digit phone number";
      isValid = false;
    }

    if (!formData.privacy) {
      newErrors.privacy = "You must agree to the privacy policy";
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value, type } = e.target;
    if (type === "checkbox") {
      const { checked } = e.target as HTMLInputElement;
      setFormData((prevState) => ({
        ...prevState,
        [name]: checked,
      }));
    } else {
      setFormData((prevState) => ({
        ...prevState,
        [name]: value,
      }));
    }

    // Clear the error for the field that's being edited
    setErrors((prevErrors) => ({
      ...prevErrors,
      [name]: "",
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      
    }
  };

  return (
    <>
      <div className="min-h-screen  py-10  relative overflow-hidden">
        <div className="relative mx-auto pb-10 px-5  md:px-14 lg:px-20 z-10 ">
          <main className="">
            <div className="relative pb-10">
              <div className="relative z-10 text-left px-2 mb-10">
                <p className="font-semibold text-[#6941C6]">Contact us</p>
                <h1 className="mt-4 text-4xl font-semibold  z-20">We’d love to hear from you</h1>
                <p className="mt-4 text-slate-300">
                  Our friendly team is always here to help.
                </p>
                <div className="">                   
                    <ContactCards/>
                    
                </div>
              </div>
            </div>

            <section className="relative mt-16 text-center">
              <div>
                <h2 className="mt-2 text-4xl font-semibold gradient-text">Get in touch</h2>
              </div>
              <form
                onSubmit={handleSubmit}
                className="mt-8 max-w-md mx-auto space-y-6 text-left"
              >
                <div>
                  <label
                    htmlFor="name"
                    className="block text-sm font-medium text-slate-300"
                  >
                    Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    id="name"
                    className="mt-1 block w-full p-2 border  rounded-lg focus:border-[#7F70ED] focus:ring-[#7F70ED] focus:outline-none"
                    placeholder="Enter your name"
                  />
                  {errors.name && (
                    <p className="text-xs text-[#D32F2F]">{errors.name}</p>
                  )}
                </div>

                <div>
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-slate-300"
                  >
                    Email
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    id="email"
                    className="mt-1 block w-full p-2 border  rounded-lg focus:border-[#7F70ED] focus:ring-[#7F70ED] focus:outline-none"
                    placeholder="you@company.com"
                  />
                  {errors.email && (
                    <p className="text-xs text-[#D32F2F]">{errors.email}</p>
                  )}
                </div>

                <div>
                  <label
                    htmlFor="phone"
                    className="block text-sm font-medium text-slate-300"
                  >
                    Phone number
                  </label>
                  <input
                    type="text"
                    name="phone"
                    id="phone"
                    value={formData.phone}
                    onChange={handleChange}
                    className="block w-full p-2 border  rounded-lg focus:border-[#7F70ED] focus:ring-[#7F70ED] focus:outline-none"
                    placeholder="85233 84666"
                  />
                  {errors.phone && (
                    <p className="text-xs text-[#D32F2F]">{errors.phone}</p>
                  )}
                </div>

                <div>
                  <label
                    htmlFor="message"
                    className="block text-sm font-medium text-slate-300"
                  >
                    Message
                  </label>
                  <textarea
                    rows={4}
                    name="message"
                    id="message"
                    value={formData.message}
                    onChange={handleChange}
                    className="mt-1 block w-full p-2 border  rounded-lg focus:border-[#7F70ED] focus:ring-[#7F70ED] focus:outline-none"
                    placeholder="Leave us a message..."
                  ></textarea>
                  {errors.message && (
                    <p className="text-xs text-[#D32F2F]">{errors.message}</p>
                  )}
                </div>

                <div className="flex items-start">
                  <div className="flex items-center h-5">
                    <input
                      id="privacy"
                      name="privacy"
                      type="checkbox"
                      checked={formData.privacy}
                      onChange={handleChange}
                      className="h-4 w-4 text-[#6941C6]  rounded focus:border-[#7F70ED] focus:ring-[#7F70ED] focus:outline-none"
                    />
                  </div>
                  <div className="ml-3 text-sm">
                    <label
                      htmlFor="privacy"
                      className="font-medium text-slate-200"
                    >
                      You agree to our friendly{" "}
                      <a href="/privacy-policy" className="text-[#6941C6]">
                        privacy policy
                      </a>
                      .
                    </label>
                    {errors.privacy && (
                      <p className="text-xs text-[#D32F2F]">{errors.privacy}</p>
                    )}
                  </div>
                </div>

                <div>
                  <button
                    type="submit"
                    className="w-full py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-[#7F70ED] hover:bg-purple-700"
                  >
                    Send message
                  </button>
                </div>
              </form>

            </section>
            
          </main>
        </div>
      </div>

      {showToast.visible && (
        <div className="fixed top-4 right-4 z-50 space-y-2 p-4">
          <div
            role="alert"
            className={`${
              showToast.success
                ? "bg-green-100 dark:bg-green-900 border-l-4 border-green-500 dark:border-green-700 text-green-900 dark:text-green-100"
                : "bg-red-100 dark:bg-red-900 border-l-4 border-red-500 dark:border-red-700 text-red-900 dark:text-red-100"
            } p-2 rounded-lg flex items-center transition duration-300 ease-in-out hover:bg-green-200 dark:hover:bg-green-800 transform hover:scale-105`}
          >
            <svg
              stroke="currentColor"
              viewBox="0 0 24 24"
              fill="none"
              className={`h-5 w-5 flex-shrink-0 mr-2 ${
                showToast.success ? "text-green-600" : "text-red-600"
              }`}
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M13 16h-1v-4h1m0-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                strokeWidth="2"
                strokeLinejoin="round"
                strokeLinecap="round"
              ></path>
            </svg>
            <p className="text-xs font-semibold">{showToast.message}</p>
          </div>
        </div>
      )}
    </>
  );
};

export default ContactUs;
