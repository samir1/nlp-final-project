require 'rubygems'
require 'sinatra'

get '/' do
  File.read('map.html')
end