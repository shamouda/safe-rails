class UsersController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    @user = User.new(user_params)
    @user.save

    render plain: user_params
  end

  def index
    render json: User.all()
  end

private
  def user_params
    params.require(:user).permit(:name, :age, :id) 
  end
end
