class UsersController < ApplicationController
  skip_before_action :verify_authenticity_token
  def create
    begin
      @user = User.new(user_params)
      @user.save!
      puts @user.id
      render json: @user

    rescue ActiveRecord::RecordInvalid
      render plain: "ERROR"
    end
  end

  def index
    render json: User.all()
  end

  def destroy
    begin
      User.find(params[:id]).destroy
      render plain: "Deleted "+params[:id]
    rescue ActiveRecord::RecordNotFound
      render plain: params[:id]+" not found!"
    end
  end

private
  def user_params
    params.require(:user).permit(:name, :age, :id) 
  end
end
