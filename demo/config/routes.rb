Rails.application.routes.draw do
  get 'welcome/index'

  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"
  root 'welcome#index'

  resources :users
  resources :simple_key_values
  resources :unique_key_values
  resources :indexed_key_values
  
  match 'simple_key_values/update_key', :to => 'simple_key_values#update_key', :via => :post
  match 'simple_key_values/get_key', :to => 'simple_key_values#get_key', :via => :post
  match 'simple_key_values/delete_key', :to => 'simple_key_values#delete_key', :via => :post
  match 'simple_key_values/destroy_key', :to => 'simple_key_values#destroy_key', :via => :post

  match 'unique_key_values/update_key', :to => 'unique_key_values#update_key', :via => :post
  match 'unique_key_values/get_key', :to => 'unique_key_values#get_key', :via => :post
  match 'unique_key_values/delete_key', :to => 'unique_key_values#delete_key', :via => :post
  match 'unique_key_values/destroy_key', :to => 'unique_key_values#destroy_key', :via => :post

  match 'indexed_key_values/update_key', :to => 'indexed_key_values#update_key', :via => :post
  match 'indexed_key_values/get_key', :to => 'indexed_key_values#get_key', :via => :post
  match 'indexed_key_values/delete_key', :to => 'indexed_key_values#delete_key', :via => :post
  match 'indexed_key_values/destroy_key', :to => 'indexed_key_values#destroy_key', :via => :post

  resources :belongs_to_users
  resources :belongs_to_departments

  resources :dbfk_users
  resources :dbfk_departments

  resources :simple_users
  resources :simple_departments

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end
