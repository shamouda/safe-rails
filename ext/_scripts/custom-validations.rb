
# PB SAFE date
comas validates_each comas/lib/date_validator.rb:127

    to = Date.parse_date(configuration.delete(:to))
    validates_each(attr_names, configuration) do |record, attr_name, value|
      before_cast = record.send("#{attr_name}_before_type_cast")
      next if allow_nil and (before_cast.nil? or before_cast == '')
      begin
        date = Date.parse_date(before_cast)
      rescue
        record.errors.add(attr_name, configuration[:message])
      else
        if from and date < from
          record.errors.add(attr_name,
                            "cannot be less than #{from.strftime('%e-%b-%Y')}")
        end
        if to and date > to
          record.errors.add(attr_name,
                            "cannot be greater than #{to.strftime('%e-%b-%Y')}")
        end
      end
    end
  end

end

# Override default date type cast class method to handle Date.parse_date
# formats (the default implementation returns nil if passed an unrecognized

# PB SAFE
comfortable-mexican-sofa validates_each comfortable-mexican-sofa/lib/comfortable_mexican_sofa/extensions/acts_as_tree.rb:40
        
        validates_each "#{configuration[:foreign_key]}" do |record, attr, value|
          if value
            if record.id == value
              record.errors.add attr, "cannot be it's own id"
            elsif record.descendants.map {|c| c.id}.include?(value)
              record.errors.add attr, "cannot be a descendant's id"
            end
          end
        end
      EOV
      
    end
  end
  
  module InstanceMethods
    # Returns list of ancestors, starting from parent until root.
    #
    #   subchild1.ancestors # => [child1, root]
    def ancestors
      node, nodes = self, []
      nodes << node = node.parent while node.parent
      nodes
    end
    

# PB SAFE just checking local state
railscollab validates_each railscollab/app/models/time_record.rb:264
  validates_presence_of :name
  validates_each :is_private, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add attr, I18n.t('not_allowed') if value == true
  end
  
  validates_each :assigned_to, :allow_nil => true do |record, attr, value|
    record.errors.add attr, I18n.t('not_part_of_project') if (!value.nil? and !value.is_part_of(record.project))
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :assigned_to_company_id
    has :assigned_to_user_id
    has :task_list_id
    has :task_id
    has :project_id
    has :is_private
    has :created_on
    has :updated_on
  end
end


# PB NOT_SAFE does a lookup WHERE; concurrent deletion; this is basically FK checking...
railscollab validates_each railscollab/app/models/time_record.rb:268
  
  validates_each :assigned_to, :allow_nil => true do |record, attr, value|
    record.errors.add attr, I18n.t('not_part_of_project') if (!value.nil? and !value.is_part_of(record.project))
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :assigned_to_company_id
    has :assigned_to_user_id
    has :task_list_id
    has :task_id
    has :project_id
    has :is_private
    has :created_on
    has :updated_on
  end
end



# PB SAFE ; checking record
railscollab validates_each railscollab/app/models/milestone.rb:275
  validates_presence_of :name
  validates_each :is_private, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == true
  end

  validates_each :assigned_to, :allow_nil => true do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if !value.nil? and !value.is_part_of(record.project)
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :assigned_to_company_id
    has :assigned_to_user_id
    has :project_id
    has :is_private
    has :created_on
    has :updated_on
  end
end


# PB NOT_SAFE does a lookup WHERE; concurrent deletion; this is basically FK checking...
railscollab validates_each railscollab/app/models/milestone.rb:279

  validates_each :assigned_to, :allow_nil => true do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if !value.nil? and !value.is_part_of(record.project)
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :assigned_to_company_id
    has :assigned_to_user_id
    has :project_id
    has :is_private
    has :created_on
    has :updated_on
  end
end


# PB SAFE checking local properties
railscollab validates_each railscollab/app/models/message.rb:130
  validates_presence_of :text
  validates_each :milestone, :allow_nil => true do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if value.project_id != record.project_id
  end

  validates_each :category do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if value && value.project_id != record.project_id
  end

  validates_each :is_private, :is_important, :anonymous_comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == true
  end

  validates_each :comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == false
  end
  
  # Indexing
  define_index do
    indexes :title
    indexes :text
    indexes tag_list(:tag), :as => :tags
    
    has :project_id
    has :category_id

# PB SAFE checking local properties
railscollab validates_each railscollab/app/models/message.rb:134

  validates_each :category do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if value && value.project_id != record.project_id
  end

  validates_each :is_private, :is_important, :anonymous_comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == true
  end

  validates_each :comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == false
  end
  
  # Indexing
  define_index do
    indexes :title
    indexes :text
    indexes tag_list(:tag), :as => :tags
    
    has :project_id
    has :category_id
    has :is_private
    has :created_on
    has :updated_on
  end

# PB SAFE checking local properties
railscollab validates_each railscollab/app/models/message.rb:138

  validates_each :is_private, :is_important, :anonymous_comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == true
  end

  validates_each :comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == false
  end
  
  # Indexing
  define_index do
    indexes :title
    indexes :text
    indexes tag_list(:tag), :as => :tags
    
    has :project_id
    has :category_id
    has :is_private
    has :created_on
    has :updated_on
  end
end


# PB SAFE checking local properties
railscollab validates_each railscollab/app/models/message.rb:142

  validates_each :comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == false
  end
  
  # Indexing
  define_index do
    indexes :title
    indexes :text
    indexes tag_list(:tag), :as => :tags
    
    has :project_id
    has :category_id
    has :is_private
    has :created_on
    has :updated_on
  end
end


# PB SAFE checking local properties

railscollab validates_each railscollab/app/models/task_list.rb:177
  validates_presence_of :name
  validates_each :milestone, :allow_nil => true do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if value.project_id != record.project_id
  end

  validates_each :is_private, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == true
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :milestone_id
    has :project_id
    has :is_private
    has :created_on
    has :updated_on
  end
end


# PB SAFE checking local properties

railscollab validates_each railscollab/app/models/task_list.rb:181

  validates_each :is_private, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == true
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :milestone_id
    has :project_id
    has :is_private
    has :created_on
    has :updated_on
  end
end


# PB SAFE checking local properties

railscollab validates_each railscollab/app/models/project_file.rb:207
  validates_presence_of :filename
  validates_each :folder, :allow_nil => true do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if value.project_id != record.project_id
  end

  validates_each :is_private, :is_important, :anonymous_comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == true
  end

  validates_each :comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == false
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :folder_id
    has :project_id
    has :is_private
    has :is_visible
    has :created_on
    has :updated_on

# PB SAFE checking local properties

railscollab validates_each railscollab/app/models/project_file.rb:211

  validates_each :is_private, :is_important, :anonymous_comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == true
  end

  validates_each :comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == false
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :folder_id
    has :project_id
    has :is_private
    has :is_visible
    has :created_on
    has :updated_on
  end
end


# PB SAFE checking local properties
railscollab validates_each railscollab/app/models/project_file.rb:215

  validates_each :comments_enabled, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
    record.errors.add(attr, I18n.t('not_allowed')) if value == false
  end
  
  # Indexing
  define_index do
    indexes :name
    indexes :description
    indexes tag_list(:tag), :as => :tags
    
    has :folder_id
    has :project_id
    has :is_private
    has :is_visible
    has :created_on
    has :updated_on
  end
end


# PB SAFE checking local properties
railscollab validates_each railscollab/app/models/comment.rb:91
	validates_presence_of :text
	validates_each :is_private, :if => Proc.new { |obj| !obj.last_edited_by_owner? } do |record, attr, value|
		record.errors.add attr, I18n.t('not_allowed') if value == true
	end
  
  # Indexing
  define_index do
    indexes :text
    
    has :project_id
    has :is_private
    has :created_on
    has :updated_on
  end
end


# PB SAFE checking local properties
railscollab validates_each railscollab/app/models/task.rb:188

  validates_each :task_list, :allow_nil => false do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if (value.project_id != record.project_id)
  end

  validates_each :assigned_to, :allow_nil => true do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if !value.nil? and !value.is_part_of(record.task_list.project)
  end
  
  # Indexing
  define_index do
    indexes :text
    
    has :assigned_to_company_id
    has :assigned_to_user_id
    has :task_list_id
    has :project_id
    has task_list(:is_private), :as => :is_private
    has :created_on
    has :updated_on
  end
end


# PB NOT_SAFE does a lookup WHERE; concurrent deletion; this is basically FK checking...
railscollab validates_each railscollab/app/models/task.rb:192

  validates_each :assigned_to, :allow_nil => true do |record, attr, value|
    record.errors.add(attr, I18n.t('not_part_of_project')) if !value.nil? and !value.is_part_of(record.task_list.project)
  end
  
  # Indexing
  define_index do
    indexes :text
    
    has :assigned_to_company_id
    has :assigned_to_user_id
    has :task_list_id
    has :project_id
    has task_list(:is_private), :as => :is_private
    has :created_on
    has :updated_on
  end
end


# PB SAFE send is equivalent to set dynamically -- weird usage of validates?
lovd-by-less validates_each lovd-by-less/vendor/gems/paperclip-2.1.2/lib/paperclip.rb:139

      validates_each(name) do |record, attr, value|
        value.send(:flush_errors)
      end
    end

    # Places ActiveRecord-style validations on the size of the file assigned. The
    # possible options are:
    # * +in+: a Range of bytes (i.e. +1..1.megabyte+),
    # * +less_than+: equivalent to :in => 0..options[:less_than]
    # * +greater_than+: equivalent to :in => options[:greater_than]..Infinity
    # * +message+: error message to display, use :min and :max as replacements
    def validates_attachment_size name, options = {}
      attachment_definitions[name][:validations] << lambda do |attachment, instance|
        unless options[:greater_than].nil?
          options[:in] = (options[:greater_than]..(1/0)) # 1/0 => Infinity
        end
        unless options[:less_than].nil?
          options[:in] = (0..options[:less_than])
        end
        unless attachment.original_filename.blank? || options[:in].include?(instance[:"#{name}_file_size"].to_i)
          min = options[:in].first
          max = options[:in].last
          
          if options[:message]

# PB NOT_SAFE sensitive to page deletions
radiant validates_each radiant/lib/plugins/active_record_extensions/lib/active_record_extensions.rb:6
    configuration = args.extract_options!
    validates_each(args, configuration) do |record, attr_name, value|
      page = Page.find_by_path(value)
      record.errors.add(attr_name, :page_not_found, :default => configuration[:message]) if page.nil? || page.is_a?(FileNotFoundPage)
    end
  end
  
  def self.object_id_attr(symbol, klass)
    module_eval %{
      def #{symbol}
        if @#{symbol}.nil? or (@old_#{symbol}_id != #{symbol}_id)
          @old_#{symbol}_id = #{symbol}_id
          klass = #{klass}.descendants.find { |d| d.#{symbol}_name == #{symbol}_id }
          klass ||= #{klass}
          @#{symbol} = klass.new
        else
          @#{symbol}
        end
      end
    }
  end
  
end


# PB SAFE just does format validation
canvas-lms validates_each canvas-lms/lib/custom_validations.rb:24
    def validates_as_url(*fields)
      validates_each(fields, :allow_nil => true) do |record, attr, value|
        begin
          value, uri = CanvasHttp.validate_url(value)

          record.send("#{attr}=", value)
        rescue URI::InvalidURIError, ArgumentError
          record.errors.add attr, 'is not a valid URL'
        end
      end
    end

    def validates_as_readonly(*fields)
      validates_each(fields) do |record, attr, value|
        if !record.new_record? && record.send("#{attr}_changed?")
          record.errors.add attr, "cannot be changed"
        end
      end
    end

    # alloweds is a hash of old_value => [new_value]
    # on update, only those transitions will be allowed for the given field
    def validates_allowed_transitions(field, alloweds)
      validates_each(field) do |record, attr, value|
        if !record.new_record? && record.send("#{attr}_changed?")

# PB SAFE just does field validation
canvas-lms validates_each canvas-lms/lib/custom_validations.rb:36
    def validates_as_readonly(*fields)
      validates_each(fields) do |record, attr, value|
        if !record.new_record? && record.send("#{attr}_changed?")
          record.errors.add attr, "cannot be changed"
        end
      end
    end

    # alloweds is a hash of old_value => [new_value]
    # on update, only those transitions will be allowed for the given field
    def validates_allowed_transitions(field, alloweds)
      validates_each(field) do |record, attr, value|
        if !record.new_record? && record.send("#{attr}_changed?")
          old_val = record.send("#{attr}_was")
          unless alloweds.any? { |old,news| old_val == old && Array(news).include?(value) }
            record.errors.add attr, "cannot be changed to that value"
          end
        end
      end
    end
  end

  def self.included(klass)
    if klass < ActiveRecord::Base
      klass.send :extend, ClassMethods

# PB SAFE just does field validation
canvas-lms validates_each canvas-lms/lib/custom_validations.rb:46
    def validates_allowed_transitions(field, alloweds)
      validates_each(field) do |record, attr, value|
        if !record.new_record? && record.send("#{attr}_changed?")
          old_val = record.send("#{attr}_was")
          unless alloweds.any? { |old,news| old_val == old && Array(news).include?(value) }
            record.errors.add attr, "cannot be changed to that value"
          end
        end
      end
    end
  end

  def self.included(klass)
    if klass < ActiveRecord::Base
      klass.send :extend, ClassMethods
    end
  end

end


# PB SAFE 
canvas-lms validates_each canvas-lms/app/models/pseudonym.rb:42
  # allows us to validate the user and pseudonym together, before saving either
  validates_each :user_id do |record, attr, value|
    record.errors.add(attr, "blank?") unless value || record.user
  end
  before_validation :validate_unique_id
  before_destroy :retire_channels

  before_save :set_password_changed
  before_validation :infer_defaults, :verify_unique_sis_user_id
  after_save :update_passwords_on_related_pseudonyms
  after_save :update_account_associations_if_account_changed
  has_a_broadcast_policy

  alias_method :context, :account

  include StickySisFields
  are_sis_sticky :unique_id

  validates_each :password, {:if => :require_password?}, &Canvas::PasswordPolicy.method("validate")
  acts_as_authentic do |config|
    config.validates_format_of_login_field_options = {:with => /\A\w[\w\.\+\-_'@ =]*\z/}
    config.login_field :unique_id
    config.validations_scope = [:account_id, :workflow_state]
    config.perishable_token_valid_for = 30.minutes
    config.validates_length_of_login_field_options = {:within => 1..MAX_UNIQUE_ID_LENGTH}

# PB SAFE just checking format
canvas-lms validates_each canvas-lms/app/models/pseudonym.rb:59

  validates_each :password, {:if => :require_password?}, &Canvas::PasswordPolicy.method("validate")
  acts_as_authentic do |config|
    config.validates_format_of_login_field_options = {:with => /\A\w[\w\.\+\-_'@ =]*\z/}
    config.login_field :unique_id
    config.validations_scope = [:account_id, :workflow_state]
    config.perishable_token_valid_for = 30.minutes
    config.validates_length_of_login_field_options = {:within => 1..MAX_UNIQUE_ID_LENGTH}
    config.validates_uniqueness_of_login_field_options = { :case_sensitive => false, :scope => [:account_id, :workflow_state], :if => lambda { |p| (p.unique_id_changed? || p.workflow_state_changed?) && p.active? } }
  end

  attr_writer :require_password
  def require_password?
    # Change from auth_logic: don't require a password just because new_record?
    # is true. just check if the pw has changed or crypted_password_field is
    # blank.
    password_changed? || (send(crypted_password_field).blank? && sis_ssha.blank?) || @require_password
  end

  acts_as_list :scope => :user

  set_broadcast_policy do |p|
    p.dispatch :confirm_registration
    p.to { self.communication_channel || self.user.communication_channel }
    p.whenever { |record|

# PB SAFE just checking format
canvas-lms validates_each canvas-lms/app/models/wiki_page.rb:154

  validates_each :title do |record, attr, value|
    if value.blank?
      record.errors.add(attr, t('errors.blank_title', "Title can't be blank"))
    elsif value.size > maximum_string_length
      record.errors.add(attr, t('errors.title_too_long', "Title can't exceed %{max_characters} characters", :max_characters => maximum_string_length))
    elsif value.to_url.blank?
      record.errors.add(attr, t('errors.title_characters', "Title must contain at least one letter or number")) # it's a bit more liberal than this, but let's not complicate things
    end
  end

  has_a_broadcast_policy
  simply_versioned :exclude => SIMPLY_VERSIONED_EXCLUDE_FIELDS, :when => Proc.new { |wp|
    # :user_id and :updated_at do not merit creating a version, but should be saved
    exclude_fields = [:user_id, :updated_at].concat(SIMPLY_VERSIONED_EXCLUDE_FIELDS).map(&:to_s)
    (wp.changes.keys.map(&:to_s) - exclude_fields).present?
  }
  after_save :remove_changed_flag


  workflow do
    state :active do
      event :unpublish, :transitions_to => :unpublished
    end
    state :unpublished do

# PB NOT_SAFE race if/when name may already be in use!
canvas-lms validates_each canvas-lms/app/models/group_category.rb:41

  validates_each :name do |record, attr, value|
    next unless record.name_changed? || value.blank?
    max_len = maximum_string_length
    max_len -= record.create_group_count.to_s.length + 1 if record.create_group_count

    if value.blank?
      record.errors.add attr, t(:name_required, "Name is required")
    elsif GroupCategory.protected_name_for_context?(value, record.context)
      record.errors.add attr, t(:name_reserved, "%{name} is a reserved name.", name: value)
    elsif record.context && record.context.group_categories.other_than(record).where(name: value).exists?
      record.errors.add attr, t(:name_unavailable, "%{name} is already in use.", name: value)
    elsif value.length > max_len
      record.errors.add attr, t(:name_too_long, "Enter a shorter category name")
    end
  end

  validates_each :group_limit do |record, attr, value|
    next if value.nil?
    record.errors.add attr, t(:greater_than_1, "Must be greater than 1") unless value.to_i > 1
  end

  validates_each :self_signup do |record, attr, value|
    next unless record.self_signup_changed?
    next if value.blank?


# PB SAFE value checking
canvas-lms validates_each canvas-lms/app/models/group_category.rb:57

  validates_each :group_limit do |record, attr, value|
    next if value.nil?
    record.errors.add attr, t(:greater_than_1, "Must be greater than 1") unless value.to_i > 1
  end

  validates_each :self_signup do |record, attr, value|
    next unless record.self_signup_changed?
    next if value.blank?
    if !record.context.is_a?(Course) && record != communities_for(record.context)
      record.errors.add :enable_self_signup, t(:self_signup_for_courses, "Self-signup may only be enabled for course groups or communities")
    elsif value != 'enabled' && value != 'restricted'
      record.errors.add attr, t(:invalid_self_signup, "Self-signup needs to be one of the following values: %{values}", values: "null, 'enabled', 'restricted'")
    elsif record.restricted_self_signup? && record.has_heterogenous_group?
      record.errors.add :restrict_self_signup, t(:cant_restrict_self_signup, "Can't restrict self-signup while a mixed-section group exists in the category")
    end
  end

  validates_each :auto_leader do |record, attr, value|
    next unless record.auto_leader_changed?
    next if value.blank?
    unless ['first', 'random'].include?(value)
      record.errors.add attr, t(:invalid_auto_leader, "AutoLeader type needs to be one of the following values: %{values}", values: "null, 'first', 'random'")
    end
  end

# PB NOT_SAFE conditional evaluation depends on current DB state; e.g., group_categories
canvas-lms validates_each canvas-lms/app/models/group_category.rb:62

  validates_each :self_signup do |record, attr, value|
    next unless record.self_signup_changed?
    next if value.blank?
    if !record.context.is_a?(Course) && record != communities_for(record.context)
      record.errors.add :enable_self_signup, t(:self_signup_for_courses, "Self-signup may only be enabled for course groups or communities")
    elsif value != 'enabled' && value != 'restricted'
      record.errors.add attr, t(:invalid_self_signup, "Self-signup needs to be one of the following values: %{values}", values: "null, 'enabled', 'restricted'")
    elsif record.restricted_self_signup? && record.has_heterogenous_group?
      record.errors.add :restrict_self_signup, t(:cant_restrict_self_signup, "Can't restrict self-signup while a mixed-section group exists in the category")
    end
  end

  validates_each :auto_leader do |record, attr, value|
    next unless record.auto_leader_changed?
    next if value.blank?
    unless ['first', 'random'].include?(value)
      record.errors.add attr, t(:invalid_auto_leader, "AutoLeader type needs to be one of the following values: %{values}", values: "null, 'first', 'random'")
    end
  end

  scope :active, -> { where(:deleted_at => nil) }

  scope :other_than, lambda { |cat| where("group_categories.id<>?", cat.id || 0) }


# PB SAFE -- if we don't hit the 'next's, we just do a local format check
canvas-lms validates_each canvas-lms/app/models/group_category.rb:74

  validates_each :auto_leader do |record, attr, value|
    next unless record.auto_leader_changed?
    next if value.blank?
    unless ['first', 'random'].include?(value)
      record.errors.add attr, t(:invalid_auto_leader, "AutoLeader type needs to be one of the following values: %{values}", values: "null, 'first', 'random'")
    end
  end

  scope :active, -> { where(:deleted_at => nil) }

  scope :other_than, lambda { |cat| where("group_categories.id<>?", cat.id || 0) }

  class << self
    def protected_name_for_context?(name, context)
      protected_names_for_context(context).include?(name)
    end

    def student_organized_for(context)
      role_category_for_context('student_organized', context)
    end

    def imported_for(context)
      role_category_for_context('imported', context)
    end

# PB NOT_SAFE ; may delete the appointment_group.contexts concurrently
canvas-lms validates_each canvas-lms/app/models/appointment_group_sub_context.rb:28

  validates_each :sub_context do |record, attr, value|
    if record.participant_type == 'User'
      record.errors.add(attr, t('errors.invalid_course_section', 'Invalid course section')) unless value.blank? || value.is_a?(CourseSection) && record.appointment_group.contexts.any? { |c| c == value.course }
    else
      record.errors.add(attr, t('errors.missing_group_category', 'Group appointments must have a group category')) unless value.present? && value.is_a?(GroupCategory)
      record.errors.add(attr, t('errors.invalid_group_category', 'Invalid group category')) unless value && record.appointment_group.contexts.any? { |c| c == value.context }
    end
  end

  def participant_type
    sub_context_type == 'GroupCategory' ? 'Group' : 'User'
  end
end


# PB NOT_SAFE e.g., enrollment limit might change depending on concurrent saves!
canvas-lms validates_each canvas-lms/app/models/user.rb:279
  validates_acceptance_of :terms_of_use, :if => :require_acceptance_of_terms, :allow_nil => false
  validates_each :self_enrollment_code do |record, attr, value|
    next unless record.require_self_enrollment_code
    if value.blank?
      record.errors.add(attr, "blank")
    elsif record.validation_root_account
      course = record.validation_root_account.self_enrollment_course_for(value)
      record.self_enrollment_course = course
      if course && course.self_enrollment_enabled?
        record.errors.add(attr, "full") if course.self_enrollment_limit_met?
        record.errors.add(attr, "already_enrolled") if course.user_is_student?(record, :include_future => true)
      else
        record.errors.add(attr, "invalid")
      end
    else
      record.errors.add(attr, "account_required")
    end
  end

  before_save :assign_uuid
  before_save :update_avatar_image
  before_save :record_acceptance_of_terms
  after_save :update_account_associations_if_necessary
  after_save :self_enroll_if_necessary


# PB NOT_SAFE ; duplicates, etc.
canvas-lms validates_each canvas-lms/app/models/calendar_event.rb:70

  validates_each :child_event_data do |record, attr, events|
    next unless events || Canvas::Plugin.value_to_boolean(record.remove_child_events)
    events ||= []
    events = events.values if events.is_a?(Hash)
    next record.errors.add(attr, t('errors.no_updating_user', "Can't update child events unless an updating_user is set")) if events.present? && !record.updating_user
    context_codes = events.map{ |e| e[:context_code] }
    next record.errors.add(attr, t('errors.duplicate_child_event_contexts', "Duplicate child event contexts")) if context_codes != context_codes.uniq
    contexts = find_all_by_asset_string(context_codes).group_by(&:asset_string)
    context_codes.each do |code|
      context = contexts[code] && contexts[code][0]
      next if context && context.grants_right?(record.updating_user, :manage_calendar) && context.try(:parent_event_context) == record.context
      break record.errors.add(attr, t('errors.invalid_child_event_context', "Invalid child event context"))
    end
    record.child_event_contexts = contexts
    record.child_event_data = events
  end

  def replace_child_events
    return unless @child_event_data
    current_events = child_events.group_by{ |e| e[:context_code] }
    @child_event_data.each do |data|
      if event = current_events.delete(data[:context_code]) and event = event[0]
        event.updating_user = @updating_user
        event.update_attributes(:start_at => data[:start_at], :end_at => data[:end_at])

# PB SAFE ; simple formatting
canvas-lms validates_each canvas-lms/app/models/group.rb:87

  validates_each :name do |record, attr, value|
    if value.blank?
      record.errors.add attr, t(:name_required, "Name is required")
    elsif value.length > maximum_string_length
      record.errors.add attr, t(:name_too_long, "Enter a shorter group name")
    end
  end

  validates_each :max_membership do |record, attr, value|
    next if value.nil?
    record.errors.add attr, t(:greater_than_1, "Must be greater than 1") unless value.to_i > 1
  end

  alias_method :participating_users_association, :participating_users

  def participating_users(user_ids = nil)
    user_ids ?
      participating_users_association.where(:id =>user_ids) :
      participating_users_association
  end

  def wiki_with_create
    Wiki.wiki_for_context(self)
  end

# PB SAFE ; formatting
canvas-lms validates_each canvas-lms/app/models/group.rb:95

  validates_each :max_membership do |record, attr, value|
    next if value.nil?
    record.errors.add attr, t(:greater_than_1, "Must be greater than 1") unless value.to_i > 1
  end

  alias_method :participating_users_association, :participating_users

  def participating_users(user_ids = nil)
    user_ids ?
      participating_users_association.where(:id =>user_ids) :
      participating_users_association
  end

  def wiki_with_create
    Wiki.wiki_for_context(self)
  end
  alias_method_chain :wiki, :create

  def auto_accept?
    self.group_category &&
    self.group_category.allows_multiple_memberships? &&
    self.join_level == 'parent_context_auto_join'
  end


# PB NOT_SAFE concurrent overlapping appointments
canvas-lms validates_each canvas-lms/app/models/appointment_group.rb:65
  validates_inclusion_of :participant_visibility, :in => ['private', 'protected'] # presumably we might add public if we decide to show appointments on the public calendar feed
  validates_each :appointments do |record, attr, value|
    next unless record.new_appointments.present? || record.validation_event_override
    appointments = value
    if record.validation_event_override
      appointments = appointments.select{ |a| a.new_record? || a.id != record.validation_event_override.id} << record.validation_event_override
    end
    appointments.sort_by(&:start_at).inject(nil) do |prev, appointment|
      record.errors.add(attr, t('errors.invalid_end_at', "Appointment end time precedes start time")) if appointment.end_at < appointment.start_at
      record.errors.add(attr, t('errors.overlapping_appointments', "Appointments overlap")) if prev && appointment.start_at < prev.end_at
      appointment
    end
  end

  def validate
    if appointment_group_contexts.empty?
      errors.add :appointment_group_contexts,
                 t('errors.needs_contexts', 'Must have at least one context')
    end
  end

  attr_accessible :title, :description, :location_name, :location_address, :contexts, :sub_context_codes, :participants_per_appointment, :min_appointments_per_participant, :max_appointments_per_participant, :new_appointments, :participant_visibility, :cancel_reason

  # when creating/updating an appointment, you can give it a list of (new)
  # appointment times. these will be added to the existing appointment times


# PB SAFE ; Resources set by conf
refinerycms FileSizeValidator refinerycms/resources/lib/refinery/resources/validators/file_size_validator.rb:3
    module Validators
      class FileSizeValidator < ActiveModel::Validator

        def validate(record)
          file = record.file

          if file.respond_to?(:length) && file.length > Resources.max_file_size
            record.errors[:file] << ::I18n.t('too_big',
                                             :scope => 'activerecord.errors.models.refinery/resource',
                                             :size => Resources.max_file_size)
          end
        end

      end
    end
  end
end


# PB SAFE: changed? => whether this actual image has changed.
refinerycms ImageUpdateValidator refinerycms/images/lib/refinery/images/validators/image_update_validator.rb:3
    module Validators
      class ImageUpdateValidator < ActiveModel::Validator

        def validate(record)
          if record.image_name_changed?
            record.errors.add :image_name,
              ::I18n.t("different_file_name",
                       :scope => "activerecord.errors.models.refinery/image")
          end
        end

      end
    end
  end
end


# PB SAFE static configuration
refinerycms ImageSizeValidator refinerycms/images/lib/refinery/images/validators/image_size_validator.rb:3
    module Validators
      class ImageSizeValidator < ActiveModel::Validator

        def validate(record)
          image = record.image

          if image.respond_to?(:length) && image.length > Images.max_image_size
            record.errors[:image] << ::I18n.t('too_big',
                                             :scope => 'activerecord.errors.models.refinery/image',
                                             :size => Images.max_image_size)
          end
        end

      end
    end
  end
end


# PB SAFE formatting only
skyline validates_each skyline/vendor/weppos/url_validation.rb:57

    validates_each(attr_names, configuration) do |record, attr_name, value|
      begin
        uri = URI.parse(value)

        if !allowed_schemes.include?(uri.scheme)
          raise(URI::InvalidURIError)
        end

        if [:scheme, :host].any? { |i| uri.send(i).blank? }
          raise(URI::InvalidURIError)
        end

      rescue URI::InvalidURIError => e
        record.errors.add(attr_name, :invalid, :default => configuration[:message], :value => value)
        next
      end
    end
  end
end

# PB SAFE formatting
communityengine validates_each communityengine/app/models/invitation.rb:12

  validates_each :email_addresses do |record, attr, email_addresses |
    invalid_emails = []
    email_addresses = email_addresses || ''
    emails = email_addresses.split(",").collect{|email| email.strip }.uniq
    
    emails.each{ |email|
      unless email =~ /[\w._%-]+@[\w.-]+.[a-zA-Z]{2,4}/
        invalid_emails << email
      end        
    }
    unless invalid_emails.empty?
      record.errors.add(:email_addresses, " included invalid addresses: <ul>"+invalid_emails.collect{|email| '<li>'+email+'</li>' }.join+"</ul>")
      record.email_addresses = (emails - invalid_emails).join(', ')
    end
  end

  attr_accessible :email_addresses, :message

  def send_invite
    emails = self.email_addresses.split(",").collect{|email| email.strip }.uniq 
    emails.each{|email|
      UserNotifier.signup_invitation(email, self.user, self.message).deliver
    }
  end

# PB SAFE formatting
communityengine validates_each communityengine/app/models/friendship.rb:14
  validate :cannot_request_if_daily_limit_reached
  validates_each :user_id do |record, attr, value|
    record.errors.add attr, 'can not be same as friend' if record.user_id.eql?(record.friend_id)
  end
  
  # named scopes
  scope :accepted, lambda {
    #hack: prevents FriendshipStatus[:accepted] from getting called before the friendship_status records are in the db (only matters in testing ENV)
    {:conditions => ["friendship_status_id = ?", FriendshipStatus[:accepted].id]    }
  }
  
  def cannot_request_if_daily_limit_reached  
    if new_record? && initiator && user.has_reached_daily_friend_request_limit?
      errors.add(:base, "Sorry, you'll have to wait a little while before requesting any more friendships.") 
    end
  end  
    
  before_validation(:on => :create){:set_pending}
  after_save :notify_requester, :if => Proc.new{|fr| fr.accepted? && fr.initiator }

  attr_protected :friendship_status_id
  
  def reverse
    Friendship.find(:first, :conditions => ['user_id = ? and friend_id = ?', self.friend_id, self.user_id])
  end

# PB SAFE ; validates against external URLs, but fine from DB 
publify validates_each publify/lib/spam_protection.rb:103

        validates_each(attr_names, configuration) do |record, attr_name, value|
          record.errors.add(attr_name, configuration[:message]) if SpamProtection.new(record.blog).is_spam?(value)
        end
      end
    end
  end
end


# PB SAFE formatting
piggybak validates_each piggybak/app/models/piggybak/payment.rb:73

    validates_each :payment_method_id do |record, attr, value|
      if record.new_record?
        credit_card = ActiveMerchant::Billing::CreditCard.new(record.credit_card)
     
        if !credit_card.valid?
          credit_card.errors.each do |key, value|
            if value.any? && !["first_name", "last_name", "type"].include?(key)
              record.errors.add key, (value.is_a?(Array) ? value.join(', ') : value)
            end
          end
        end
      end
    end
  end
end

# PB SAFE formatting
piggybak validates_each piggybak/app/models/piggybak/payment_method.rb:14

    validates_each :payment_method_values do |record, attr, value|
      if record.klass.present?
        payment_method = record.klass.constantize
        metadata_keys = value.collect { |v| v.key }.sort
        if payment_method::KEYS.sort != metadata_keys
          if payment_method::KEYS.empty?
            record.errors.add attr, "You don't need any metadata for this method."
          else
            record.errors.add attr, "You must define key values for #{payment_method::KEYS.join(', ')} for this payment method."
          end
        end
      end
    end
    validates_each :active do |record, attr, value|
      if value && PaymentMethod.where(active: true).select { |p| p != record }.size > 0
        record.errors.add attr, "You may only have one active payment method."
      end
    end

    def key_values
      self.metadata.inject({}) { |h, k| h[k.key.to_sym] = k.value; h }
    end

    def admin_label

# PB NOT_SAFE false; may not set active:false
piggybak validates_each piggybak/app/models/piggybak/payment_method.rb:27
    end
    validates_each :active do |record, attr, value|
      if value && PaymentMethod.where(active: true).select { |p| p != record }.size > 0
        record.errors.add attr, "You may only have one active payment method."
      end
    end

    def key_values
      self.metadata.inject({}) { |h, k| h[k.key.to_sym] = k.value; h }
    end

    def admin_label
      "#{self.description}"
    end
  end
end


# PB SAFE validation
piggybak validates_each piggybak/app/models/piggybak/tax_method.rb:10

    validates_each :tax_method_values do |record, attr, value|
      if record.klass.present?
        calculator = record.klass.constantize
        metadata_keys = value.collect { |v| v.key }.sort
        if calculator::KEYS.sort != metadata_keys
          if calculator::KEYS.empty?
            record.errors.add attr, "You don't need any metadata for this method."
          else
            record.errors.add attr, "You must define key values for #{calculator::KEYS.join(', ')} for this tax method."
          end
        end
      end
    end

    def klass_enum 
      Piggybak.config.tax_calculators
    end

    def self.calculate_tax(object)
      total_tax = 0

      TaxMethod.all.each do |tax_method|
        calculator = tax_method.klass.constantize
        if calculator.available?(tax_method, object)


# PB SAFE formatting
piggybak validates_each piggybak/app/models/piggybak/shipping_method.rb:10

    validates_each :shipping_method_values do |record, attr, value|
      if record.klass.present?
        calculator = record.klass.constantize
        metadata_keys = value.collect { |v| v.key }.sort
        if calculator::KEYS.sort != metadata_keys
          if calculator::KEYS.empty?
            record.errors.add attr, "You don't need any metadata for this method."
          else
            record.errors.add attr, "You must define key values for #{calculator::KEYS.join(', ')} for this shipping method."
          end
        end
      end
    end

    def klass_enum
      Piggybak.config.shipping_calculators.collect { |b| [ b.constantize.description, b ] }
    end

    def self.available_methods(cart)
      active_methods = ShippingMethod.where(active: true)

      active_methods.select { |method| method.klass.constantize.available?(method, cart) }
    end


# PB NOT_SAFE present?, deleted? can be racy
teambox validates_each teambox/app/models/reset_password.rb:7
  validates_format_of :email, :on => :create, :unless => Proc.new{|p|p.email.blank?}, :with => /^([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,})$/i, :message => 'is not a valid email address'
  validates_each :user, :unless => Proc.new{|p|p.errors[:email].present?} do |record, attr, value|
    record.errors.add attr, "doesn\'t exist in the system." if record.user.nil? or record.user.deleted?
  end
  
  before_create :create_code

  protected
  
  def create_code
    self.reset_code = ActiveSupport::SecureRandom.hex(20)
    self.expiration_date = 2.weeks.from_now
  end
end


# PB SAFE BANNED_USERNAMES is static
lobsters validates_each lobsters/app/models/user.rb:41

  validates_each :username do |record,attr,value|
    if BANNED_USERNAMES.include?(value.to_s.downcase)
      record.errors.add(attr, "is not permitted")
    end
  end

  before_save :check_session_token
  before_validation :on => :create do
    self.create_rss_token
    self.create_mailing_list_token
  end

  BANNED_USERNAMES = [ "admin", "administrator", "hostmaster", "mailer-daemon",
    "postmaster", "root", "security", "support", "webmaster", "moderator",
    "moderators", ]

  # days old accounts are considered new for
  NEW_USER_DAYS = 7

  def self.recalculate_all_karmas!
    User.all.each do |u|
      u.karma = u.stories.map(&:score).sum + u.comments.map(&:score).sum
      u.save!
    end

# PB NOT_SAFE could concurrently remove from project
openproject validates_each openproject/app/models/category.rb:42
  # validates that assignee is member of the issue category's project
  validates_each :assigned_to_id do |record, attr, value|
    if value # allow nil
      record.errors.add(attr, l(:error_must_be_project_member)) unless record.project.principals.map(&:id).include? value
    end
  end

  safe_attributes 'name', 'assigned_to_id'

  alias :destroy_without_reassign :destroy

  # Destroy the category
  # If a category is specified, issues are reassigned to this category
  def destroy(reassign_to = nil)
    if reassign_to && reassign_to.is_a?(Category) && reassign_to.project == self.project
      WorkPackage.update_all("category_id = #{reassign_to.id}", "category_id = #{id}")
    end
    destroy_without_reassign
  end

  def <=>(category)
    name <=> category.name
  end

  def to_s; name end

# PB NOT_SAFE could concurrently decrement quantity!
spree AvailabilityValidator spree/core/app/models/spree/stock/availability_validator.rb:2
  module Stock
    class AvailabilityValidator < ActiveModel::Validator
      def validate(line_item)
        unit_count = line_item.inventory_units.size
        return if unit_count >= line_item.quantity
        quantity = line_item.quantity - unit_count

        quantifier = Stock::Quantifier.new(line_item.variant)

        unless quantifier.can_supply? quantity
          variant = line_item.variant
          display_name = %Q{#{variant.name}}
          display_name += %Q{ (#{variant.options_text})} unless variant.options_text.blank?

          line_item.errors[:quantity] << Spree.t(:selected_quantity_not_available, :scope => :order_populator, :item => display_name.inspect)
        end
      end
    end
  end
end


# PB NOT_SAFE default_tax resolves to Zone.where(default_tax: true).first
spree DefaultTaxZoneValidator spree/core/app/models/spree/tax_rate.rb:1
module Spree
  class DefaultTaxZoneValidator < ActiveModel::Validator
    def validate(record)
      if record.included_in_price
        record.errors.add(:included_in_price, Spree.t(:included_price_validation)) unless Zone.default_tax
      end
    end
  end
end

module Spree
  class TaxRate < Spree::Base
    acts_as_paranoid
    include Spree::CalculatedAdjustments
    include Spree::AdjustmentSource
    belongs_to :zone, class_name: "Spree::Zone", inverse_of: :tax_rates
    belongs_to :tax_category, class_name: "Spree::TaxCategory", inverse_of: :tax_rates

    has_many :adjustments, as: :source

    validates :amount, presence: true, numericality: true
    validates :tax_category_id, presence: true
    validates_with DefaultTaxZoneValidator

    before_destroy :deals_with_adjustments_for_deleted_source

# PB SAFE formatting
spree DbMaximumLengthValidator spree/core/app/models/spree/validations/db_maximum_length_validator.rb:4
    # Validates a field based on the maximum length of the underlying DB field, if there is one.
    class DbMaximumLengthValidator < ActiveModel::Validator

      def initialize(options)
        super
        @field = options[:field].to_s
        raise ArgumentError.new("a field must be specified to the validator") if @field.blank?
      end

      def validate(record)
        limit = record.class.columns_hash[@field].limit
        value = record[@field.to_sym]
        if value && limit && value.to_s.length > limit 
          record.errors.add(@field.to_sym, :too_long, count: limit)
        end
      end
    end
  end
end


# PB SAFE ; internationalization formatting
onebody validates_each onebody/app/models/relationship.rb:13
  validates_uniqueness_of :other_name, scope: [:site_id, :name, :person_id, :related_id]
  validates_each :name do |record, attribute, value|
    unless I18n.t('relationships.names').keys.map(&:to_s).include?(value) or value == 'other'
      record.errors.add attribute, :inclusion
    end
  end

  def name_or_other
    name == 'other' ? other_name : I18n.t(name, scope: 'relationships.names')
  end

  def reciprocate
    if can_auto_reciprocate?
      Relationship.create(person: related, related: person, name: reciprocal_name)
    end
  end

  def reciprocal_name
    RECIPROCAL_RELATIONSHIP_NAMES[name][person.gender]
  end

  def can_auto_reciprocate?
    !reciprocal_name.nil?
  end


# PB NOT_SAFE concurrent Family insertion
onebody validates_each onebody/app/models/family.rb:29

  validates_each [:barcode_id, :alternate_barcode_id] do |record, attribute, value|
    if attribute.to_s == 'barcode_id' and record.barcode_id
      if record.barcode_id == record.alternate_barcode_id
        record.errors.add(attribute, :taken)
      elsif Family.where(alternate_barcode_id: record.barcode_id).count > 0
        record.errors.add(attribute, :taken)
      end
    elsif attribute.to_s == 'alternate_barcode_id' and record.alternate_barcode_id
      if Family.where(barcode_id: record.alternate_barcode_id).count > 0
        record.errors.add(attribute, :taken)
      end
    end
  end

  def initialize(*args)
    super
    self.country = Setting.get(:system, :default_country) unless country.present?
  end

  geocoded_by :location
  after_validation :geocode

  def barcode_id=(b)
    write_attribute(:barcode_id, b.to_s.strip.any? ? b : nil)

# PB SAFE formatting
onebody validates_each onebody/app/models/message.rb:28

  validates_each :to_person_id, allow_nil: true do |record, attribute, value|
    if attribute.to_s == 'to_person_id' and value and record.to and record.to.email.nil?
      record.errors.add attribute, :invalid
    end
  end

  validates_each :body do |record, attribute, value|
    if attribute.to_s == 'body' and value.to_s.blank? and record.html_body.to_s.blank?
      record.errors.add attribute, :blank
    end
  end

  def name
    if self.to
      "Private Message to #{to.name rescue '[deleted]'}"
    elsif parent
      "Reply to \"#{parent.subject}\" in Group #{top.group.name rescue '[deleted]'}"
    else
      "Message \"#{subject}\" in Group #{group.name rescue '[deleted]'}"
    end
  end

  def top
    top = self

# PB SAFE formatting
onebody validates_each onebody/app/models/message.rb:34

  validates_each :body do |record, attribute, value|
    if attribute.to_s == 'body' and value.to_s.blank? and record.html_body.to_s.blank?
      record.errors.add attribute, :blank
    end
  end

  def name
    if self.to
      "Private Message to #{to.name rescue '[deleted]'}"
    elsif parent
      "Reply to \"#{parent.subject}\" in Group #{top.group.name rescue '[deleted]'}"
    else
      "Message \"#{subject}\" in Group #{group.name rescue '[deleted]'}"
    end
  end

  def top
    top = self
    while top.parent
      top = top.parent
    end
    return top
  end


# PB NOT_SAFE ; can change settings during save
discourse Validators::UploadValidator discourse/lib/validators/upload_validator.rb:4

class Validators::UploadValidator < ActiveModel::Validator

  def validate(upload)
    extension = File.extname(upload.original_filename)[1..-1] || ""

    if is_authorized?(upload, extension)
      if FileHelper.is_image?(upload.original_filename)
        authorized_image_extension(upload, extension)
        maximum_image_file_size(upload)
      else
        authorized_attachment_extension(upload, extension)
        maximum_attachment_file_size(upload)
      end
    end
  end

  def is_authorized?(upload, extension)
    authorized_extensions(upload, extension, authorized_uploads)
  end

  def authorized_image_extension(upload, extension)
    authorized_extensions(upload, extension, authorized_images)
  end


# PB NOT_SAFE e.g., max_posts_validator and concurrent posts
discourse Validators::PostValidator discourse/lib/validators/post_validator.rb:2
module Validators; end
class Validators::PostValidator < ActiveModel::Validator
  def validate(record)
    presence(record)
    unless Discourse.static_doc_topic_ids.include?(record.topic_id) && record.acting_user.try(:admin?)
      stripped_length(record)
      raw_quality(record)
      max_posts_validator(record)
      max_mention_validator(record)
      max_images_validator(record)
      max_attachments_validator(record)
      max_links_validator(record)
      unique_post_validator(record)
    end
  end

  def presence(post)
    [:raw,:topic_id].each do |attr_name|
       post.errors.add(attr_name, :blank, options) if post.send(attr_name).blank?
    end
    if post.new_record? and post.user_id.nil?
      post.errors.add(:user_id, :blank, options)
    end
  end


