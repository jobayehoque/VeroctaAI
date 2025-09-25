import React from 'react'
import { UsersIcon, LightBulbIcon, GlobeAltIcon } from '@heroicons/react/24/outline'

const About: React.FC = () => {
  const values = [
    {
      icon: LightBulbIcon,
      title: 'Innovation',
      description: 'We constantly push the boundaries of what\'s possible with AI technology.'
    },
    {
      icon: UsersIcon,
      title: 'Collaboration',
      description: 'We work closely with our clients to ensure solutions meet their exact needs.'
    },
    {
      icon: GlobeAltIcon,
      title: 'Global Impact',
      description: 'Our solutions help businesses worldwide achieve their AI transformation goals.'
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 to-secondary-50 section-padding">
        <div className="container-max text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            About <span className="text-gradient">VEROCTA</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            We are a team of passionate AI experts dedicated to transforming businesses 
            through innovative artificial intelligence solutions.
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="section-padding bg-white">
        <div className="container-max">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-gray-600 mb-6">
                At VEROCTA, we believe that artificial intelligence has the power to 
                revolutionize how businesses operate and grow. Our mission is to make 
                advanced AI technology accessible, practical, and impactful for organizations 
                of all sizes.
              </p>
              <p className="text-lg text-gray-600">
                We combine cutting-edge research with real-world business experience to 
                deliver AI solutions that drive measurable results and create lasting value 
                for our clients.
              </p>
            </div>
            <div className="bg-gradient-to-br from-primary-100 to-secondary-100 rounded-2xl p-8">
              <div className="text-center">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Our Vision</h3>
                <p className="text-gray-700">
                  To be the leading provider of AI solutions that empower businesses to 
                  achieve their full potential through intelligent automation, data-driven 
                  insights, and innovative problem-solving.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="section-padding bg-gray-50">
        <div className="container-max">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Our Core Values
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              These fundamental principles guide everything we do and shape how we 
              work with our clients and partners.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {values.map((value, index) => (
              <div key={index} className="card text-center hover:shadow-xl transition-shadow duration-300">
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <value.icon className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {value.title}
                </h3>
                <p className="text-gray-600">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="section-padding bg-white">
        <div className="container-max">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Our Team
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Meet the talented individuals behind FinDash's innovative solutions.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {/* Team Member Placeholder */}
            <div className="card text-center">
              <div className="w-24 h-24 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-white text-2xl font-bold">JD</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">John Doe</h3>
              <p className="text-primary-600 font-medium mb-3">CEO & Founder</p>
              <p className="text-gray-600 text-sm">
                AI expert with 15+ years of experience in machine learning and business transformation.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-24 h-24 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-white text-2xl font-bold">JS</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Jane Smith</h3>
              <p className="text-primary-600 font-medium mb-3">CTO</p>
              <p className="text-gray-600 text-sm">
                Technology leader specializing in scalable AI infrastructure and cloud solutions.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-24 h-24 bg-gradient-to-br from-primary-400 to-secondary-400 rounded-full mx-auto mb-4 flex items-center justify-center">
                <span className="text-white text-2xl font-bold">MJ</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Mike Johnson</h3>
              <p className="text-primary-600 font-medium mb-3">Head of AI Research</p>
              <p className="text-gray-600 text-sm">
                Research scientist focused on cutting-edge AI algorithms and neural networks.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default About
